#!/usr/bin/env python3
"""Run with python3 tests/test_task_brief.py [path/to/task-brief]."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = (Path(sys.argv.pop(1)) if len(sys.argv) > 1 else
          Path(__file__).resolve().parents[1] / "skills/subagent-driven-development/scripts/task-brief").resolve()
SENTINEL = b"previous complete result\n"


class TaskBriefTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="task-brief-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plan = self.root / "plan with spaces.md"
        self.output = self.root / "brief with spaces.md"

    def run_helper(self, text, task="1", output=None):
        self.plan.write_bytes(text.encode("utf-8"))
        return subprocess.run(["bash", str(HELPER), str(self.plan), task,
                               str(output or self.output)], capture_output=True, text=True)

    def assert_success(self, text, expected, task="1"):
        result = self.run_helper(text, task)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_text(), expected)

    def test_canonical_korean_and_legacy_headings(self):
        for heading in ("### Task 1: 입력 검증", "# Task 1 - Legacy"):
            with self.subTest(heading=heading):
                task = heading + "\n필수 요구사항\n#### 1. 검증 조건\nACCEPTANCE\n\n"
                self.assert_success(task + "### Task 2: 다음 작업\nNEXT\n", task)

    def test_fenced_task_examples_preserve_acceptance(self):
        for opener, middle, closer in (
            ("```markdown", "", "```"),
            ("~~~markdown", "", "~~~"),
            ("````markdown", "```\n~~~\n# Task 10: still literal\n", "`````"),
            ("~~~~markdown", "~~~\n```\n# Task 10: still literal\n", "~~~~~"),
            ("   ~~~markdown", "  ~~~ trailing text\n# Task 10: literal\n", "   ~~~  "),
            ("  ```markdown", "  ``` trailing text\n# Task 10: literal\n", "  ```\t"),
        ):
            with self.subTest(opener=opener):
                task = f"### Task 1: 입력 검증\n{opener}\n# Task 2: literal\n{middle}{closer}\nACCEPTANCE\n\n"
                self.assert_success(task + "### Task 2: 실제 다음 작업\nNEXT\n", task)

    def test_numbered_overview_is_not_a_task(self):
        task = "### Task 1: 입력 검증\nBODY\nACCEPTANCE\n\n"
        for heading in ("## 1. 범위", "### 1. 배경"):
            with self.subTest(heading=heading):
                text = heading + "\n공통 목표\n\n" + task + "### Task 2: 다음\nNEXT\n"
                self.assert_success(text, task)

    def test_line_endings_preserve_original_bytes(self):
        for fence in ("```", "~~~"):
            for newline in ("\n", "\r\n"):
                with self.subTest(fence=fence, newline=repr(newline)):
                    task = f"### Task 1: 입력 검증\n{fence}text\n# Task 2: literal\n{fence}\nACCEPTANCE\n\n"
                    task = task.replace("\n", newline)
                    text = task + "### Task 2: 다음\nNEXT\n".replace("\n", newline)
                    result = self.run_helper(text)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(self.output.read_bytes(), task.encode("utf-8"))

    def test_numbers_do_not_collide(self):
        first = "### Task 1: One\nONE\n\n"
        tenth = "### Task 10: Ten\nTEN\n"
        self.assert_success(first + tenth, first)
        self.assert_success(first + tenth, tenth, "10")
        large = "### Task 9007199254740993: Large\nLARGE\n"
        self.assert_success(first + large, large, "9007199254740993")

    def test_invalid_plans_preserve_previous_output(self):
        cases = {
            "missing": "### Task 2: Other\nOTHER\n",
            "numeric-heading": "### 1. 입력 검증\nBODY\n",
            "duplicate": "### Task 1: A\nA\n### Task 1: B\nB\n",
            "unclosed-tilde": "### Task 1: A\n~~~\nBODY\n",
            "unclosed-backtick": "### Task 1: A\n```\nBODY\n",
            "unclosed-crlf": "### Task 1: A\r\n~~~\r\nBODY\r\n",
            "numeric-task-sibling": "### Task 1: A\nBODY\n### 2. B\nNEXT\n",
        }
        for name, text in cases.items():
            with self.subTest(case=name):
                self.output.write_bytes(SENTINEL)
                result = self.run_helper(text)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.output.read_bytes(), SENTINEL)
                self.assertTrue(result.stderr.strip())
                self.assertEqual(list(self.root.glob(".*.tmp.*")), [])
                self.assertEqual(list(self.root.glob(".*.err.*")), [])

    def test_invalid_numbers_preserve_previous_output(self):
        for number in ("0", "-1", "abc", "1.5", "01"):
            with self.subTest(number=number):
                self.output.write_bytes(SENTINEL)
                result = self.run_helper("### Task 1: Valid\nBODY\n", number)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.output.read_bytes(), SENTINEL)

    def test_plan_aliases_cannot_be_output(self):
        text = "### Task 1: Valid\nBODY\n"
        self.plan.write_text(text)
        link = self.root / "plan-link.md"
        hardlink = self.root / "plan-hardlink.md"
        link.symlink_to(self.plan)
        hardlink.hardlink_to(self.plan)
        for output in (self.plan, link, hardlink):
            with self.subTest(output=output.name):
                result = self.run_helper(text, output=output)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.plan.read_text(), text)

    def test_directory_output_is_rejected_without_writes(self):
        directory = self.root / "output-directory"
        directory.mkdir()
        result = self.run_helper("### Task 1: Valid\nBODY\n", output=directory)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(directory.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
