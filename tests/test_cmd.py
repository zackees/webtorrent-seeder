import os
import unittest


class CmdTester(unittest.TestCase):
    """Tester for running the webtorrent_seeder cmd."""

    def test_cmd(self) -> None:
        """Print the help text for the webtorrent_seeder."""
        self.assertEqual(0, os.system('webtorrent_seeder -h'))


if __name__ == "__main__":
    unittest.main()
