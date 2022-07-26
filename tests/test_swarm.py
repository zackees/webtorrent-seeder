import os
import unittest
import tempfile

from webtorrent_seeder.peer import PeerProcess, create_peer
from webtorrent_seeder.seed import SeedProcess, create_file_seeder

HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(HERE)
TEST_MP4 = os.path.join(PROJECT_ROOT, "test.mp4")

DEFAULT_TRACKERLIST = ["wss://webtorrent-tracker.onrender.com:80"]
EXPECTED_MAGNET_URI = "magnet:?xt=urn:btih:4053f84988c249c7efa6643ddc0867c939d30737&dn=test.mp4&tr=wss%3A%2F%2Fwebtorrent-tracker.onrender.com"

class SwarmTester(unittest.TestCase):
    """Tester for running the webtorrent_seeder cmd."""

    def test_test_mp4(self) -> None:
        """Seed a test.mp4 file."""
        seed_process: SeedProcess = create_file_seeder(
            filepath=TEST_MP4,
            tracker_list=DEFAULT_TRACKERLIST,
        )
        magnet_uri = seed_process.wait_for_magnet_uri()
        self.assertEqual(EXPECTED_MAGNET_URI, magnet_uri)
        peer_process: PeerProcess = create_peer(
            magnet_uri=seed_process.magnet_uri)
        assert seed_process is not None
        assert peer_process is not None
        seed_process.terminate()
        peer_process.terminate()
        expected_file = os.path.join(HERE, "test.mp4")
        if os.path.exists(expected_file):
            os.remove(expected_file)


if __name__ == "__main__":
    unittest.main()
