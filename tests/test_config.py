import os
import unittest
from verbum.config.config import Source, Config


class TestConfig(unittest.TestCase):
    def test_source(self):
        s = Source(file="file", template="template")
        s.validate()

        s.__dict__.pop("file")
        self.assertRaisesRegex(AttributeError, "file", s.validate)
        s.__dict__["file"] = "file"

        s.__dict__.pop("template")
        self.assertRaisesRegex(AttributeError, "template", s.validate)
        s.__dict__["template"] = "template"

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
