
"""
Peer for sharing a file.
"""


import subprocess


class PeerProcess:  # pylint: disable=too-few-public-methods
    """Seeder process."""

    def __init__(self, magnet_uri: str, output_dir: str | None = None) -> None:
        self.magnet_uri = magnet_uri
        cmd = f"webtorrent-hybrid seed {magnet_uri} --keep-seeding"
        self.process = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, cwd=output_dir, shell=True, stdout=subprocess.PIPE, universal_newlines=True
        )

    def terminate(self) -> None:
        """Kill the seeder process."""
        self.process.terminate()
        self.process.kill()

    def wait(self) -> None:
        """Waits for ctrl-c, sig-kill or terminate() to be called."""
        try:
            self.process.wait()
        except KeyboardInterrupt:
            self.terminate()
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Exception happened while waiting: {exc}")
            self.terminate()


def create_peer(magnet_uri) -> PeerProcess:
    """Runs the command to seed the content."""
    return PeerProcess(magnet_uri=magnet_uri)
