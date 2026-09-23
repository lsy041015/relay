#!/usr/bin/env python3
"""Relay removes only worktrees it created."""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/finishing-a-development-branch/SKILL.md"


class WorktreeCleanupTests(unittest.TestCase):
    def test_cleanup_requires_ownership_marker(self):
        blocks = [body for _, body in re.findall(
            r"^([ \t]*)```bash\n(.*?)^\1```[ \t]*$",
            SKILL.read_text(), re.S | re.M)]
        cleanup = next(body for body in blocks if 'git worktree remove "$WORKTREE_PATH"' in body)
        for owned in (False, True):
            with self.subTest(owned=owned), tempfile.TemporaryDirectory(prefix="worktree-cleanup-") as temp:
                repo = Path(temp) / "repo"
                repo.mkdir()
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                subprocess.run(["git", "-C", str(repo), "-c", "user.name=Fixture",
                                "-c", "user.email=fixture@example.invalid", "commit",
                                "-q", "--allow-empty", "-m", "baseline"], check=True)
                worktree = repo / ".worktrees/user"
                subprocess.run(["git", "-C", str(repo), "worktree", "add", "-q", "-b",
                                "user", str(worktree)], check=True)
                git_dir = subprocess.run(["git", "-C", str(worktree), "rev-parse",
                                          "--git-dir"], check=True, capture_output=True,
                                         text=True).stdout.strip()
                if owned:
                    (Path(git_dir) / "relay-owned-worktree").write_text(str(worktree) + "\n")
                script = f'set -eu\nGIT_DIR="{git_dir}"\nWORKTREE_PATH="{worktree}"\n' + cleanup
                result = subprocess.run(["bash", "-c", script], cwd=repo,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((worktree / ".git").exists(), not owned)


if __name__ == "__main__":
    unittest.main(verbosity=2)
