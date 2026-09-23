#!/usr/bin/env python3
"""Regression tests for SDD workspace safety and task completion."""
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "skills/subagent-driven-development/scripts/sdd-workspace"
TASK_DONE = ROOT / "skills/executing-plans/scripts/task-done"


class SddSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sdd-safety-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.plan = self.root / "plan.md"
        self.plan.write_text("# Plan\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def run_script(self, script, *args):
        return subprocess.run(["bash", str(script), *map(str, args)], cwd=self.root,
                              capture_output=True, text=True)

    def test_workspace_rejects_symlink_outside_repo(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.root / ".superpowers").symlink_to(outside, target_is_directory=True)
        result = self.run_script(WORKSPACE, self.plan)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_workspace_preserves_existing_ignore_file(self):
        base = self.root / ".superpowers/sdd"
        base.mkdir(parents=True)
        (base / ".gitignore").write_text("# keep me")
        result = self.run_script(WORKSPACE, self.plan)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((base / ".gitignore").read_text(), "# keep me\n*\n")

    def test_task_done_records_successful_silent_command(self):
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture",
                        "-c", "user.email=fixture@example.invalid", "commit",
                        "-q", "--allow-empty", "-m", "baseline"], check=True)
        sha = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"],
                             check=True, capture_output=True, text=True).stdout.strip()
        result = self.run_script(TASK_DONE, self.plan, 1, sha, "--", "true")
        self.assertEqual(result.returncode, 0, result.stderr)
        ledger = self.root / ".superpowers/sdd/plan/progress.md"
        self.assertIn("Task 1: complete", ledger.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
