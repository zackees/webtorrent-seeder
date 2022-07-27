"""
Module handles the seeding of a file.
"""

import os
import subprocess
import threading
import time
from typing import List, Optional, Tuple
from urllib.parse import urlparse


def parse_url(url: str) -> Tuple[str, int]:
    """Parses the url and returns the hostname."""
    parse_result = urlparse(url)
    url_info = parse_result.netloc.split(":")
    tracker_url = url_info[0]
    port = 80
    if len(url_info) == 2:
        port = int(url_info[1])
    url_no_port = parse_result._replace(netloc=tracker_url).geturl()
    return url_no_port, port


class SeedProcess:  # pylint: disable=too-few-public-methods
    """Seeder process."""

    def __init__(
        self, filepath: str, tracker_list: List[str],
        torrent_port: Optional[int] = None,
    ) -> None:
        # Use a regex to split out the url and the port, being mindful of the schema
        # and the port.
        assert os.path.exists(filepath), f"File {filepath} does not exist!"
        if len(tracker_list) != 1:
            raise ValueError(
                f"Only one tracker allowed at this pointm, got {tracker_list} instead"
            )
        self.file_name = filepath
        tracker_url, port = parse_url(tracker_list[0])
        self.magnet_uri = None
        cmd_list = [
            "webtorrent", "seed", filepath, "--keep-seeding",
            "--announce", tracker_url, "--port", str(port),
        ]
        if torrent_port is not None:
            cmd_list.extend(["--torrent-port", str(torrent_port)])
        cmd = ' '.join(cmd_list)
        # Iterate through the lines of stdout
        # iterate read line
        self.process = subprocess.Popen(  # pylint: disable=consider-using-with
            cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True
        )
        # This is a process to seed an actual file.
        self.thread_stdout_drain = threading.Thread(
            target=self._stdout_runner, daemon=True
        )
        self.thread_stdout_drain.start()
        self.alive = True

    def terminate(self) -> None:
        """Kill the seeder process."""
        self.process.terminate()
        self.process.kill()
        self.alive = False
        if self.thread_stdout_drain:
            self.process.stdout.close()  # type: ignore
            self.thread_stdout_drain.join(timeout=1)
            if self.thread_stdout_drain.is_alive():
                print("Warning, seed stdout drain thread still active.")
        print(f"seeder killed for {self.file_name}.")

    def wait(self) -> None:
        """Waits for ctrl-c, sig-kill or terminate() to be called."""  # pylint: disable
        try:
            self.process.wait()
        except KeyboardInterrupt:
            self.terminate()
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Exception happened while waiting: {exc}")
            self.terminate()

    def wait_for_magnet_uri(self, timeout=60) -> str:
        """Waits for the magnet URI to be found."""
        expired_time = time.time() + timeout
        while self.magnet_uri is None:
            if time.time() > expired_time:
                raise TimeoutError(
                    f"Timeout waiting for magnet URI for {self.file_name}"
                )
            time.sleep(0.1)
        return self.magnet_uri

    def _stdout_runner(self) -> None:
        try:
            for line in iter(self.process.stdout.readline, b""):  # type: ignore
                if not self.alive:
                    return
                if self.magnet_uri is None:
                    if line.startswith("magnetURI: "):
                        self.magnet_uri = line.split(" ")[1].strip()
        except ValueError:
            # Thrown when self.process.stdout is closed during shutdown.
            pass

    def __del__(self):
        self.terminate()


def create_file_seeder(
    filepath: str,
    tracker_list: List[str],
) -> SeedProcess:
    """Runs the command to seed the content."""
    return SeedProcess(filepath=filepath, tracker_list=tracker_list)
