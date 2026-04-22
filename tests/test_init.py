import os
import re
import tempfile
import unittest
from typing import List, Optional

from src.verbm.init import init_project
from src.verbm.version_control.git import Git
from src.verbm.version_control.interface import VersionControl


class FakeVC(VersionControl):
    def __init__(
        self,
        last_tag: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ):
        self._last_tag = last_tag
        self._username = username
        self._email = email

    def add(self, *files: str):
        pass

    def commit(self, message: str, username: Optional[str], email: Optional[str]):
        pass

    def tag(self, tag: str):
        pass

    def push(self, with_tags: bool):
        pass

    def log(self, from_tag: str, file_filters: List[re.Pattern]) -> List[str]:
        return []

    def last_tag(self) -> Optional[str]:
        return self._last_tag

    def username(self) -> Optional[str]:
        return self._username

    def email(self) -> Optional[str]:
        return self._email


class TestInit(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.file = os.path.join(self.dir, "version.yml")

    def tearDown(self):
        self._tmp.cleanup()

    def test_init_twice(self):
        git = Git()

        init_project(self.dir, git)
        self.assertRaises(Exception, init_project, self.dir, git)

    def test_no_last_tag(self):
        vc = FakeVC(last_tag=None, username="Jane", email="jane@example.com")

        init_project(self.dir, vc)

        with open(self.file) as f:
            content = f.read()

        self.assertIn("0.0.0", content)
        self.assertIn("Jane", content)

    def test_unparseable_tag(self):
        vc = FakeVC(last_tag="not-a-version", username="Jane", email="jane@example.com")

        init_project(self.dir, vc)

        with open(self.file) as f:
            content = f.read()

        self.assertIn("0.0.0", content)

    def test_placeholders(self):
        vc = FakeVC(last_tag="v2.3.4", username=None, email=None)

        init_project(self.dir, vc)

        with open(self.file) as f:
            content = f.read()

        self.assertIn("2.3.4", content)
        self.assertIn("John Doe", content)
        self.assertIn("john.doe@example.com", content)


if __name__ == "__main__":
    unittest.main()
