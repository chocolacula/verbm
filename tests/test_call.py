import unittest
from src.verbm.version_control.call import call


class TestGit(unittest.TestCase):

    def test_call(self):
        out = call("ls", "-la")
        n = len(out.split("\n"))

        self.assertGreater(n, 1)

        # negative, wrong argument with "--"
        self.assertRaises(Exception, call, "ls", "--la")


if __name__ == "__main__":
    unittest.main()
