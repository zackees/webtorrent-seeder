"""
Module handles the seeding of a file.
"""

import os
import subprocess
import threading
import time
from typing import List, Tuple
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


class SeederProcess:  # pylint: disable=too-few-public-methods
    """Seeder process."""

    def __init__(
        self, file_name: str, magnet_uri: str, process: subprocess.Popen
    ) -> None:
        self.file_name = file_name
        self.magnet_uri = magnet_uri
        self.process = process
        if file_name is not None:
            # This is a process to seed an actual file.
            self.thread_stdout_drain = threading.Thread(
                target=self._stdout_runner, daemon=True
            )
            self.thread_stdout_drain.start()
        else:
            self.thread_stdout_drain = None
        self.error = None
        self.alive = True

    def terminate(self) -> None:
        """Kill the seeder process."""
        self.process.terminate()
        self.process.kill()
        if self.thread_stdout_drain:
            self.thread_stdout_drain.join(timeout=1)
            if self.thread_stdout_drain.is_alive():
                print("Warning, seed stdout drain thread still active.")
        self.alive = False
        print(f"seeder killed for {self.file_name}.")

    def wait(self) -> None:
        """Waits for ctrl-c, sig-kill or terminate() to be called."""
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
        print("starting stdout drain")
        for line in iter(self.process.stdout.readline, b""):  # type: ignore
            if not self.alive:
                return
            if self.magnet_uri is None:
                if line.startswith("magnetURI: "):
                    self.magnet_uri = line.split(" ")[1].strip()

    def __del__(self):
        self.terminate()


def seed_file(
    path: str,
    tracker_list: List[str],
) -> SeederProcess:
    """Runs the command to seed the content."""
    assert os.path.exists(path), f"File {path} does not exist!"
    if len(tracker_list) != 1:
        raise ValueError(
            f"Only one tracker allowed at this pointm, got {tracker_list} instead"
        )
    # Use a regex to split out the url and the port, being mindful of the schema
    # and the port.
    tracker_url, port = parse_url(tracker_list[0])
    cmd = f"webtorrent-hybrid seed {path} --keep-seeding --announce {tracker_url} --port {port}"
    # Iterate through the lines of stdout
    # iterate read line
    process = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True
    )
    return SeederProcess(file_name=path, magnet_uri=None, process=process)


def seed_magneturi(magnet_uri) -> SeederProcess:  # Never returns.
    """Runs the command to seed the content."""
    # Use a regex to split out the url and the port, being mindful of the schema
    # and the port.
    cmd = f"webtorrent-hybrid seed {magnet_uri} --keep-seeding"
    # Iterate through the lines of stdout
    # iterate read line
    process = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True
    )
    return SeederProcess(file_name=None, magnet_uri=magnet_uri, process=process)
