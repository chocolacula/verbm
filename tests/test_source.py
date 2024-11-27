import unittest

from src.verbum.source import SourceManager
from src.verbum.version import Version
from src.verbum.config.config import Config


class TestSource(unittest.TestCase):
    def test_consistent(self):
        c = Config.from_file("./tests/data/source/consistent/version.yaml")
        sm = SourceManager(c.path, c.source)

        v = Version(c.template, c.version)

        self.assertTrue(sm.consistent(v))

        c = Config.from_file("./tests/data/source/inconsistent/version.yaml")
        sm = SourceManager(c.path, c.source)

        v = Version(c.template, c.version)

        self.assertFalse(sm.consistent(v))

        c = Config.from_file("./tests/data/source/invalid/version.yaml")
        sm = SourceManager(c.path, c.source)

        v = Version(c.template, c.version)

        self.assertRaises(Exception, sm.consistent, v)

    def test_replace(self):
        pass

    def test_files(self):
        pass


if __name__ == "__main__":
    unittest.main()
