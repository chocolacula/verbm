import os
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from src.verbm.version_control.git import Git


class TestGitFilter(unittest.TestCase):
    """Unit tests for Git.log parsing — `call` is mocked, no real git invoked."""

    delim = ">+>:+-\n"

    def _log_output(self, entries):
        # entries: list of (subject, body, files) tuples, mirroring git log --pretty=format
        parts = [""]
        for subject, body, files in entries:
            commit_chunk = subject + "\n" + body
            files_chunk = "\n" + "\n".join(files)
            parts.append(commit_chunk)
            parts.append(files_chunk)
        return self.delim.join(parts) + self.delim

    def test_log_no_filters_returns_all_commits(self):
        g = Git()
        raw = self._log_output(
            [
                ("feat: a new thing", "", ["src/a.py"]),
                ("fix: a bug", "detail", ["src/b.py"]),
            ]
        )
        with patch("src.verbm.version_control.git.call", return_value=raw):
            commits = g.log("v1.0.0", [])

        self.assertIn("feat: a new thing", commits)
        self.assertIn("fix: a bug", commits)
        self.assertIn("detail", commits)

    def test_log_with_filter_keeps_matching(self):
        g = Git()
        raw = self._log_output(
            [
                ("feat: python change", "", ["src/a.py"]),
                ("feat: docs change", "", ["README.md"]),
            ]
        )
        with patch("src.verbm.version_control.git.call", return_value=raw):
            commits = g.log("v1.0.0", [re.compile(r".*\.py$")])

        self.assertIn("feat: python change", commits)
        self.assertNotIn("feat: docs change", commits)

    def test_log_when_rev_parse_fails(self):
        g = Git()
        raw = self._log_output([("feat: x", "", ["a.py"])])

        # First call (rev-parse) raises, second (log) returns data.
        calls = [Exception("no such tag"), raw]

        def fake_call(*args, **kwargs):
            result = calls.pop(0)
            if isinstance(result, Exception):
                raise result
            return result

        with patch("src.verbm.version_control.git.call", side_effect=fake_call):
            commits = g.log("v0.0.0", [])

        self.assertIn("feat: x", commits)


@unittest.skipIf(shutil.which("git") is None, "git binary not available")
class TestGitIntegration(unittest.TestCase):
    """Smoke tests against a disposable real git repo."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = self._tmp.name
        self._cwd = os.getcwd()
        os.chdir(self.repo)

        subprocess.run(["git", "init", "-q", "-b", "main"], check=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Tester"], check=True)

        with open("file.txt", "w") as f:
            f.write("hello\n")

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def test_add_commit_tag_last_tag(self):
        g = Git()
        g.add("file.txt")
        g.commit("feat: initial", username=None, email=None)
        g.tag("v0.1.0")

        self.assertEqual(g.last_tag(), "v0.1.0")

    def test_username_and_email(self):
        g = Git()
        self.assertEqual(g.username(), "Tester")
        self.assertEqual(g.email(), "t@t.com")

    def test_last_tag_none_when_no_tags(self):
        g = Git()
        # fresh repo, no commits/tags
        self.assertIsNone(g.last_tag())

    def test_current_sha_none_before_any_commit(self):
        g = Git()
        self.assertIsNone(g.current_sha())

    def test_current_sha_after_commit(self):
        g = Git()
        g.add("file.txt")
        g.commit("feat: initial", username="Alt", email="alt@x.com")
        sha = g.current_sha()
        self.assertIsNotNone(sha)
        self.assertEqual(len(sha), 40)  # type: ignore


if __name__ == "__main__":
    unittest.main()
