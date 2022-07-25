"""
Runs installation and starts seeding.
"""

import argparse
import os
import subprocess
import sys
from typing import List

from webtorrent_seeder.seeder import seed_file, seed_magneturi

DEFAULT_TRACKERS = ["wss://webtorrent-tracker.onrender.com"]


def has_cmd(cmd):
    """
    Checks if a command is available.
    """
    try:
        subprocess.check_output(f"which {cmd}", shell=True, stderr=subprocess.STDOUT)
    except Exception:  # pylint: disable=broad-exception
        return False
    return True


def uninstall() -> int:
    """Uninstall node"""
    print(
        "Uninstalling webtorrent_seeder node dependencies,"
        " which will auto-install the next time the command runs."
    )
    rtn: int = os.system("npm uninstall -g webtorrent_seeder")
    rtn += os.system("npm uninstall -g node-gyp-build")
    return rtn


def install_node_deps(reinstall: bool = False) -> None:
    """Installs any missing node dependencies for the command to run."""
    if reinstall:
        uninstall()
    if not has_cmd("node-gyp-build"):
        os.system("npm install -g node-gyp-build")
    if not has_cmd("webtorrent-hybrid"):
        os.system("npm install -g https://github.com/zackees/webtorrent-hybrid")
    assert has_cmd("webtorrent-hybrid")


def main() -> int:
    """Runs the installation and starts seeding."""
    parser = argparse.ArgumentParser(
        description="Runs installation and starts seeding.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # First positional argument is the url to the video
    parser.add_argument("magnet_or_path", help="The magnet_or_path to the content.", nargs="?")
    # Add repeating argument for additional trackers
    parser.add_argument(
        "-t",
        "--trackers",
        nargs="*",
        help="Additional trackers to use.",
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
    # parser.add_argument("--install", action="store_true", help="Runs installation.")
    # Unconditionally run node-gyp-build, since it's so fast to install.
    magnet_or_path = args.magnet_or_path or input("Enter the file path or the magnetURI: ")
    trackers: List[str] = args.trackers
    print(args)
    print("magnet_or_path: ", magnet_or_path)
    if args.reinstall:
        uninstall()
    install_node_deps()
    if "magnet" in magnet_or_path:
        seed_magneturi(magnet_uri=magnet_or_path)
    else:
        seed_file(path=magnet_or_path, trackers=trackers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
