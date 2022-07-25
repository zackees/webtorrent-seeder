import os
import unittest

HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)
TEST_MP4 = os.path.join(PROJECT_ROOT, "test.mp4")


class CmdTester(unittest.TestCase):
    """Tester for running the webtorrent_seeder cmd."""

    def test_cmd(self) -> None:
        """Print the help text for the webtorrent_seeder."""
        self.assertEqual(0, os.system("webtorrent_seeder -h"))

    def test_test_mp4(self) -> None:
        """Seed a test.mp4 file."""
        self.assertTrue(os.path.exists(TEST_MP4))


if __name__ == "__main__":
    unittest.main()
