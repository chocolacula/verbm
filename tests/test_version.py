import unittest
from src.verbum.version import Version


class TestVersion(unittest.TestCase):
    def test_init_parse(self):
        format = "v$major.$minor.$patch"
        version = "v1.2.3"

        v = Version(format)
        v.parse(version)

        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)

        format = "v$major.$patch.$minor"  # wrong order
        v = Version(format, version)

        self.assertEqual(v.major, 1)
        self.assertEqual(v.patch, 2)
        self.assertEqual(v.minor, 3)

        self.assertRaises(Exception, v.parse, "3.4.5")  # without 'v'

    def test_str(self):
        format = "v$major.$minor.$patch"
        version = "v1.2.3"

        v = Version(format, version)
        v.major = 3

        self.assertEqual(str(v), "v3.2.3")


if __name__ == "__main__":
    unittest.main()
