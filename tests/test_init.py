import os
import unittest
from src.verbum.init import init_project
from src.verbum.version_control.git import Git


class TestInit(unittest.TestCase):

    def test_init(self):
        git = Git()

        init_project("./tests/data", git)

        self.assertRaises(Exception, init_project, "./tests/data", git)

        os.remove("./tests/data/version.yml")


if __name__ == "__main__":
    unittest.main()