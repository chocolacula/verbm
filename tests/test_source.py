import copy
import os
from typing import Tuple
import unittest

from src.verbm.source import SourceManager
from src.verbm.version import Version
from src.verbm.config.config import Config


class TestSource(unittest.TestCase):
    def test_consistent(self):
        def prepare(filename: str) -> Tuple[SourceManager, Version]:
            c = Config.from_file(filename)
            sm = SourceManager(c.path, c.source)
            v = Version(c.template, c.version)

            return sm, v

        sm, v = prepare("./tests/data/source/consistent/version.yaml")
        self.assertTrue(sm.consistent(v))

        sm, v = prepare("./tests/data/source/inconsistent/version.yaml")
        self.assertFalse(sm.consistent(v))

        sm, v = prepare("./tests/data/source/invalid/version.yaml")
        self.assertRaises(Exception, sm.consistent, v)

    def test_replace(self):
        c = Config.from_file("./tests/data/source/consistent/version.yaml")
        sm = SourceManager(c.path, c.source)

        v1 = Version(c.template, c.version)
        self.assertTrue(sm.consistent(v1))

        v2 = copy.copy(v1)
        v2.patch += 1

        sm.replace(v1, v2)
        self.assertTrue(sm.consistent(v2))

        sm.replace(v2, v1)  # revert back
        self.assertTrue(sm.consistent(v1))

    def test_files(self):
        c = Config.from_file("./tests/data/source/consistent/version.yaml")
        sm = SourceManager(c.path, c.source)

        for f in sm.files():
            self.assertTrue(os.path.exists(f))


if __name__ == "__main__":
    unittest.main()
