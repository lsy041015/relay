#!/usr/bin/env python3
"""Run with python3 tests/test_worktree_instructions.py [path/to/SKILL.md]."""
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

SKILL = (Path(sys.argv.pop(1)) if len(sys.argv) > 1 else
         Path(__file__).resolve().parents[1] / "skills/using-git-worktrees/SKILL.md").resolve()


class WorktreeInstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blocks = [body for _, body in re.findall(
            r"^([ \t]*)```bash\n(.*?)^\1```[ \t]*$", SKILL.read_text(), re.S | re.M)]
        cls.selection = next(body for body in blocks if "LOCATION=.worktrees" in body)
        cls.safety = next(body for body in blocks if "repo_root=" in body and "check-ignore" in body)
        cls.creation = next(body for body in blocks if " worktree add " in body)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="worktree-instructions-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.subdir = self.root / "src"
        self.subdir.mkdir()
        (self.root / "worktrees").mkdir()
        (self.root / ".gitignore").write_text("worktrees/\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)

    def run_flow(self, cwd, create=False):
        script = "set -eu\n" + self.selection + "\n" + self.safety
        if create:
            script += "\n" + self.creation
        script += '\nprintf "SELECTED=%s\\n" "$selected"'
        return subprocess.run(["bash", "-c", script], cwd=cwd, capture_output=True, text=True,
                              env={**os.environ, "BRANCH_NAME": "codex/test-worktree"})

    def test_existing_directory_selected_from_any_cwd(self):
        for cwd in (self.root, self.subdir):
            with self.subTest(cwd=cwd.name):
                result = self.run_flow(cwd)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f"SELECTED={self.root}/worktrees\n", result.stdout)

    def test_preferred_directory_requires_its_own_ignore_rule(self):
        (self.root / ".worktrees").mkdir()
        result = self.run_flow(self.subdir)
        self.assertEqual(result.returncode, 1, result.stderr)
        (self.root / ".gitignore").write_text("worktrees/\n.worktrees/\n")
        result = self.run_flow(self.subdir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"SELECTED={self.root}/.worktrees\n", result.stdout)

    def test_creation_uses_selected_root_from_subdirectory(self):
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture",
                        "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                        "-c", "core.hooksPath=/dev/null", "commit", "-q", "--allow-empty",
                        "-m", "fixture baseline"], check=True, capture_output=True)
        result = self.run_flow(self.subdir, create=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = self.root / "worktrees/codex/test-worktree"
        self.assertTrue((expected / ".git").is_file())
        self.assertFalse((self.root / ".worktrees").exists())
        actual = subprocess.run(["git", "-C", str(expected), "rev-parse", "--show-toplevel"],
                                check=True, capture_output=True, text=True)
        self.assertEqual(Path(actual.stdout.strip()), expected)
        git_dir = subprocess.run(["git", "-C", str(expected), "rev-parse", "--git-dir"],
                                 check=True, capture_output=True, text=True).stdout.strip()
        self.assertEqual((Path(git_dir) / "relay-owned-worktree").read_text().strip(),
                         str(expected))


if __name__ == "__main__":
    unittest.main(verbosity=2)
