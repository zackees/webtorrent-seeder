# Brief

A command line tool to initiate a webtorrent swarm (seeding) around a file.

# Usage

```
> python -m pip install webtorrent_seeder
> webtorrent_seeder myfile.mp4
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

If the docker instance runs then it will automatically seed the `test.mp4` file and the the user should inspect that the file peer is working by going to:

[Link](https://webtorrentseeder.com?magnet=magnet%3A%3Fxt%3Durn%3Abtih%3A4053f84988c249c7efa6643ddc0867c939d30737%26dn%3Dtest.mp4%26tr%3Dwss%253A%252F%252Fwebtorrent-tracker.onrender.com)


# Todo:

  * Implement seeding by magneturi

# Versions

  * 1.0.0: Initial commit.
