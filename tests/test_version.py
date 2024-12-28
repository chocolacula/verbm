import unittest
from src.verbm.version import Version


class TestVersion(unittest.TestCase):
    def test_init_parse(self):
        format = "v$major.$minor.$patch"
        version = "v1.2.3"

        # the first version
        v = Version(format, "v0.0.0")
        self.assertEqual(str(v), "v0.0.0")

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

    def test_components(self):
        v = Version("$major.$minor.$patch", "1.2.3")
        self.assertEqual(str(v), "1.2.3")

        v = Version("$major.$minor", "1.2")
        self.assertEqual(str(v), "1.2")

        v = Version("$major", "1")
        self.assertEqual(str(v), "1")

        # at least `major` component is required
        self.assertRaises(Exception, Version, "$major", "")
        self.assertRaises(Exception, Version, "$minor", "2")
        self.assertRaises(Exception, Version, "$patch", "3")

        # components are numbers
        self.assertRaises(Exception, Version, "$major.$minor.$patch", "foo.foo.foo")
        self.assertRaises(Exception, Version, "$major.$minor", "foo.foo")
        self.assertRaises(Exception, Version, "$major", "foo")

    def test_suffix(self):
        format = "v$major.$minor.$patch$suffix"
        version = "v1.2.3-rc"

        v = Version(format, version)
        self.assertEqual(str(v), "v1.2.3-rc")
        self.assertIsNotNone(v.suffix)
        self.assertEqual(v.suffix, "-rc")


if __name__ == "__main__":
    unittest.main()
