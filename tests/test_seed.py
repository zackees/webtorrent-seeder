import os
import unittest
from unittest.mock import DEFAULT

from webtorrent_seeder.seeder import SeederProcess, seed_file, seed_magneturi

HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)
TEST_MP4 = os.path.join(PROJECT_ROOT, "test.mp4")

DEFAULT_TRACKERLIST = ["wss://webtorrent-tracker.onrender.com:80"]

EXPECTED_MAGNET_URI = "magnet:?xt=urn:btih:4053f84988c249c7efa6643ddc0867c939d30737&dn=test.mp4&tr=wss%3A%2F%2Fwebtorrent-tracker.onrender.com"

class SeedTester(unittest.TestCase):
    """Tester for running the webtorrent_seeder cmd."""

    def test_test_mp4(self) -> None:
        """Seed a test.mp4 file."""
        seed_process: SeederProcess = seed_file(
            path=TEST_MP4,
            tracker_list=DEFAULT_TRACKERLIST,
        )
        magnet_uri = seed_process.wait_for_magnet_uri(timeout=15)
        self.assertEqual(EXPECTED_MAGNET_URI, magnet_uri)


if __name__ == "__main__":
    unittest.main()
