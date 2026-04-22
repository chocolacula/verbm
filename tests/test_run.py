import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src.verbm.run import run


def _run(argv):
    out = io.StringIO()
    with patch.object(sys, "argv", ["verbm", *argv]), redirect_stdout(out):
        try:
            run()
        except SystemExit:
            pass
    return out.getvalue()


CONFIG_YAML = """version: 0.1.0
template: $major.$minor.$patch

source:
  - file: ./main.txt
    template: VERSION = "$version"

version_control:
  commit:
    username: Tester
    email: t@t.com
    message: Version bumped from $version to $new_version
  tag: v$new_version
  matcher:
    major:
      - '^feat!: '
    minor:
      - '^feat: '
    patch:
      - '^fix: '
"""


class TestRun(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = self._tmp.name
        self._cwd = os.getcwd()
        os.chdir(self.repo)

        with open("version.yml", "w") as f:
            f.write(CONFIG_YAML)
        with open("main.txt", "w") as f:
            f.write('VERSION = "0.1.0"\n')

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def test_version_flag(self):
        out = _run(["--version"])
        self.assertRegex(out.strip(), r"^\d+\.\d+\.\d+")

    def test_get(self):
        out = _run(["get"])
        self.assertIn("0.1.0", out)

    def test_validate(self):
        out = _run(["validate"])
        self.assertIn("0.1.0", out)

    def test_up_patch(self):
        _run(["up", "patch"])
        with open("version.yml") as f:
            self.assertIn("0.1.1", f.read())
        with open("main.txt") as f:
            self.assertIn("0.1.1", f.read())

    def test_up_minor(self):
        with open("main.txt", "w") as f:
            f.write('VERSION = "0.1.0"\n')

        # bump twice to prove patch resets
        _run(["up", "patch"])
        _run(["up", "minor"])

        with open("version.yml") as f:
            self.assertIn("0.2.0", f.read())
        with open("main.txt") as f:
            self.assertIn("0.2.0", f.read())

    def test_down_minor(self):
        _run(["down", "minor"])

        with open("version.yml") as f:
            self.assertIn("0.0.0", f.read())
        with open("main.txt") as f:
            self.assertIn("0.0.0", f.read())

    def test_down_negative_raises(self):
        # version is 0.1.0 — down major would go to -1
        with self.assertRaises(Exception):
            _run(["down", "major"])

    def test_set(self):
        _run(["set", "2.3.4"])

        with open("version.yml") as f:
            self.assertIn("2.3.4", f.read())
        with open("main.txt") as f:
            self.assertIn("2.3.4", f.read())

    def test_inconsistent_raises(self):
        with open("main.txt", "w") as f:
            f.write('VERSION = "9.9.9"\n')
        with self.assertRaises(Exception):
            _run(["validate"])


@unittest.skipIf(shutil.which("git") is None, "git binary not available")
class TestRunUpAuto(unittest.TestCase):
    """End-to-end `up auto` against a temp git repo."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = self._tmp.name
        self._cwd = os.getcwd()
        os.chdir(self.repo)

        subprocess.run(["git", "init", "-q", "-b", "main"], check=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], check=True)
        subprocess.run(["git", "config", "user.name", "test"], check=True)

        # seed commit so the tagged commit has a parent (needed for rev^..HEAD)
        with open("README", "w") as f:
            f.write("seed\n")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-q", "-m", "chore: seed"], check=True)

        with open("version.yml", "w") as f:
            f.write(CONFIG_YAML)
        with open("main.txt", "w") as f:
            f.write('VERSION = "0.1.0"\n')

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-q", "-m", "chore: initial"], check=True)
        subprocess.run(["git", "tag", "v0.1.0"], check=True)

        # add a fix commit so `up auto` picks patch
        with open("main.txt", "a") as f:
            f.write("# trivial\n")

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-q", "-m", "fix: small thing"], check=True)

    def tearDown(self):
        os.chdir(self._cwd)
        self._tmp.cleanup()

    def test_picks_patch(self):
        _run(["up", "auto"])

        with open("main.txt") as f:
            self.assertIn("0.1.1", f.read())


if __name__ == "__main__":
    unittest.main()
