import os
import unittest
from src.verbum.config.config import Source, Config


class TestConfig(unittest.TestCase):
    def test_config(self):
        os.chdir("tests/data")

        # doesn't raise
        _ = Config.from_file("valid.yml")

        self.assertRaises(Exception, Config.from_file)

        self.assertRaisesRegex(  #
            TypeError, "ver", Config.from_file, "invalid-version.yml"
        )
        self.assertRaisesRegex(  #
            TypeError, "template", Config.from_file, "invalid-template.yml"
        )


if __name__ == "__main__":
    unittest.main()
