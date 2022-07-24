import os
import subprocess
import threading

# Import dataclass
from typing import List


def seed_file(path: str, trackers: List[str], port: int=80) -> None:  # Never returns.
    """Runs the command to seed the content."""
    print(f"Run command {path} {trackers}")
    trackers = ",".join(trackers)
    cmd = f'webtorrent-hybrid seed {path} --keep-seeding --announce {trackers} --port {port}'
    # Iterate through the lines of stdout
    # iterate read line
    print(f"Running: {cmd}")
    process = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True
    )
    magnet_uri: str
    for line in iter(process.stdout.readline, ""):  # type: ignore
        print(line, end="")
        if line.startswith("magnetURI: "):
            magnet_uri = line.split(" ")[1].strip()
            print("Found magnetURI!")
            break
    else:
        rtn_code = process.poll()
        if rtn_code is not None and rtn_code != 0:
            print(f"Process exited with non-zero exit code: {rtn_code}")
        else:
            print("Could not find magnetURI!")
            process.kill()
        return None
    # may freeze without draining the stdout buffer
    def drain_stdout(process: subprocess.Popen) -> None:
        for _ in iter(process.stdout.readline, ""):  # type: ignore
            continue  # just drain the stdout buffer

    thread_stdout_drain = threading.Thread(target=drain_stdout, args=(process,), daemon=True)
    thread_stdout_drain.start()
    print(f"Seeding magnet URI:\n{magnet_uri}")
    process.wait()
    


def seed_magneturi(magnet_uri) -> None:  # Never returns.
    """Runs the command to seed the content."""
    raise NotImplementedError("seed_magneturi is not implemented")
