import os
import unittest

from pydantic import ValidationError
from src.verbm.config.config import Config


class TestConfig(unittest.TestCase):
    def test_config(self):
        root = "./tests/data/config"

        valid_dir = root + "/valid"
        filenames = next(os.walk(valid_dir), (None, None, []))[2]

        for filename in filenames:
            # doesn't raise
            _ = Config.from_file(valid_dir + "/" + filename)

        self.assertRaises(Exception, Config.from_file)

        self.assertRaisesRegex(
            ValidationError,
            "ver",
            Config.from_file,
            root + "/invalid/version.yml",
        )
        self.assertRaisesRegex(
            ValidationError,
            "template",
            Config.from_file,
            root + "/invalid/template.yml",
        )


if __name__ == "__main__":
    unittest.main()
