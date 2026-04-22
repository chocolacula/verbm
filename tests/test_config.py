import os
import shutil
import tempfile
import unittest

from pydantic import ValidationError
from src.verbm.config.config import Config


class TestConfig(unittest.TestCase):
    def test_parse(self):
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

    def test_missing_path(self):
        self.assertRaisesRegex(
            Exception,
            "no such file",
            Config.from_file,
            "./tests/data/does-not-exist.yml",
        )

    def test_default_filename(self):
        cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            self.assertRaisesRegex(Exception, "cannot find", Config.from_file, None)

            src = f"{cwd}/tests/data/config/valid/no-source.yml"
            dst = "./version.yml"
            shutil.copy(src, dst)

            cfg = Config.from_file(None)
            self.assertEqual(cfg.path, "version.yml")

            os.remove(dst)
        os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
