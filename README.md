# webtorrent-seeder


[![Actions Status](https://github.com/zackees/webtorrent-seeder/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/webtorrent-seeder/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/webtorrent-seeder/workflows/Win_Tests/badge.svg)](https://github.com/zackees/webtorrent-seeder/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/webtorrent-seeder/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/webtorrent-seeder/actions/workflows/push_ubuntu.yml)



# Brief

A command line tool to initiate a webtorrent swarm (seeding) around a file. This is essentially a wrapper
around `webtorrent` but with certain fixes applied, including:
  * Merged `webtorrent-hybrid` fixes into `webtorrent`
  * Unconditionally prints out the magnet uri.

# Usage (Command Line)

Starting a webtorrent swarm:
```
> python -m pip install webtorrent_seeder
> webtorrent_seeder myfile.mp4 --trackers "wss://webtorrent-tracker.onrender.com:80"
```

Joining a webtorrent swarm:
```
> webtorrent_seeder magnet:?xt=urn:btih:4053f84988c249c7efa6643ddc0867c939d30737&dn=test.mp4&tr=wss%3A%2F%2Fwebtorrent-tracker.onrender.com
```

# Usage (API)

Initiating seeding

```py
from webtorrent_seeder.seed import SeedProcess, create_file_seeder
seed_process: SeedProcess = create_file_seeder(
    "file.mp4",
    tracker_list=["wss://webtorrent-tracker.onrender.com:80"]
)
magnet_uri = seed_process.wait_for_magnet_uri()
print(f"Found magnet: {magnet_uri}")
seed_process.wait()  # Blocks until ctrl-c signaled.

```

Joining a swarm
```py
from webtorrent_seeder.peer import PeerProcess, create_peer
peer_process: PeerProcess = create_peer(
    magnet_uri=MAGNET_URI
)
seed_process.wait()  # Blocks until ctrl-c signaled.
```

# Testing

```
> webtorrent_seeder_test
```

# If something goes wrong

Try uninstalling the npm dependencies:

```
> webtorrent_seeder_uninstall
```

Then the next run of `webtorrent_seeder` will re-install the dependencies.


# Docker Demo

If the docker instance runs then it will automatically seed the `test.mp4` file and output:

`magnet:?xt=urn:btih:4053f84988c249c7efa6643ddc0867c939d30737&dn=test.mp4&tr=wss%3A%2F%2Fwebtorrent-tracker.onrender.com`

and the the user should inspect that the file peer is working by going to:

[Link](https://webtorrentseeder.com?magnet=magnet%3A%3Fxt%3Durn%3Abtih%3A4053f84988c249c7efa6643ddc0867c939d30737%26dn%3Dtest.mp4%26tr%3Dwss%253A%252F%252Fwebtorrent-tracker.onrender.com)


# Todo:

  * Implement seeding by magneturi

# Versions
  * 1.1.2: Adds torrent port.
  * 1.1.1: Now this package exclusively uses zackees/webtorrent-cli, which has
           been merged with zackees/webtorrent-hybrid
  * 1.1.0: Rewrite of the peer/seeding mechanism + more tests.
  * 1.0.13: Port is now part of the tracker url
  * 1.0.11: Lots of fixes exposed by additional testing
  * 1.0.5: Cumalitive bug fixes
  * 1.0.2: nit
  * 1.0.1: Disallows empty magnet uri
  * 1.0.0: Initial commit.
