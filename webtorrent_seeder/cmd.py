"""
Runs installation and starts seeding.
"""

import argparse
import os
import platform
import sys
import tempfile
import urllib.parse
from shutil import which
from typing import List

from download import download  # type: ignore

from webtorrent_seeder.seeder import seed_file, seed_magneturi

TEST_DATA_URL = (
    "https://raw.githubusercontent.com/zackees/webtorrent-seeder/main/test.mp4"
)
DEFAULT_TRACKERS = ["wss://webtorrent-tracker.onrender.com"]


def has_cmd(cmd) -> bool:
    """Check whether `cmd` is on PATH and marked as executable."""
    return which(cmd) is not None


def uninstall() -> int:
    """Uninstall node"""
    print(
        "Uninstalling webtorrent_seeder node dependencies,"
        " which will auto-install the next time the command runs."
    )
    rtn: int = os.system("npm uninstall --location=global webtorrent_seeder")
    return rtn


def install_node_deps(reinstall: bool = False) -> None:
    """Installs any missing node dependencies for the command to run."""
    if reinstall:
        uninstall()
    if not has_cmd("webtorrent-hybrid"):
        os.system(
            "npm install --location=global https://github.com/zackees/webtorrent-hybrid"
        )
    if not has_cmd("webtorrent-hybrid"):
        # If sys platform is darwin m1
        if sys.platform == "darwin":
            if platform.uname().machine == "arm64":
                raise OSError(
                    "Darwin arm64 may not be not supported because of missing webrtc"
                )
        else:
            raise OSError("webtorrent-hybrid failed to install.")


def install() -> int:
    """Uninstall node"""
    install_node_deps(reinstall=False)
    return 0


def live_test() -> int:
    """Does a live test, downloading the resource necessary to seed a file."""
    # Create a temporary directory that will be deleted on close
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Download TEST_DATA_URL
        path = download(TEST_DATA_URL, os.path.join(tmpdirname, "test.mp4"))
        try:
            process = seed_file(path, tracker_list=DEFAULT_TRACKERS, verbose=True)
            print(f"\nSeeding!\nmagnet_uri:\n{process.magnet_uri}\n")
            encoded = urllib.parse.quote(process.magnet_uri, safe="")
            live_test_url = f"https://webtorrentseeder.com?magnet={encoded}"
            print(f"\nLive test url:\n{live_test_url}\n")
            process.wait()
        finally:
            os.remove(path)
    return 0


def main() -> int:
    """Runs the installation and starts seeding."""
    parser = argparse.ArgumentParser(
        description="Runs installation and starts seeding.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # First positional argument is the url to the video
    parser.add_argument(
        "magnet_or_path", help="The magnet_or_path to the content.", nargs="?"
    )
    # Add repeating argument for additional trackers
    parser.add_argument(
        "-t",
        "--trackers",
        nargs="*",
        help=f"Sets the tracker, the default is {DEFAULT_TRACKERS}.",
        default=DEFAULT_TRACKERS,
    )
    # Adds uninstall option
    parser.add_argument(
        "-u",
        "--reinstall",
        action="store_true",
        help="Uninstalls the webtorrent_seeder.",
    )
    args = parser.parse_args()  # pylint: disable=unused-variable
    magnet_or_path = args.magnet_or_path or input(
        "Enter the file path or the magnetURI: "
    )
    magnet_or_path = magnet_or_path.strip()
    if not magnet_or_path:
        raise OSError("Magnet file can't be skipped.")
    trackers: List[str] = args.trackers
    print(args)
    print("magnet_or_path:", magnet_or_path)
    if args.reinstall:
        uninstall()
    install_node_deps()
    if "magnet" in magnet_or_path.lower():
        proc = seed_magneturi(magnet_uri=magnet_or_path)
        assert proc
        proc.wait()
    else:
        proc = seed_file(path=magnet_or_path, tracker_list=trackers)
        assert proc
        proc.wait()
    return 0


if __name__ == "__main__":
    sys.exit(main())
