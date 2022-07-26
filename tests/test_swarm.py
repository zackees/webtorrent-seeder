import os
import unittest
from unittest.mock import DEFAULT

from webtorrent_seeder.seeder import SeederProcess, seed_file, seed_magneturi

HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)
TEST_MP4 = os.path.join(PROJECT_ROOT, "test.mp4")

DEFAULT_TRACKERLIST = ["wss://webtorrent-tracker.onrender.com:80"]


class SwarmTester(unittest.TestCase):
    """Tester for running the webtorrent_seeder cmd."""

    @unittest.skip("not implemented")
    def test_test_mp4(self) -> None:
        """Seed a test.mp4 file."""
        print("starting seed process")
        seed_process: SeederProcess | None = seed_file(
            path=TEST_MP4,
            tracker_list=DEFAULT_TRACKERLIST,
            verbose=True
        )
        print("seed process started")
        print("starting seed peer")
        peer_process: SeederProcess | None = seed_magneturi(
            magnet_uri=seed_process.magnet_uri,
            verbose=True)
        print("seed peer started")
        assert seed_process is not None
        assert peer_process is not None
        seed_process.terminate()
        peer_process.terminate()


if __name__ == "__main__":
    unittest.main()
