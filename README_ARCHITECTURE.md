Videoswarm: Architecture for Decentralized Video

# Centralization vs Decentralization

There's two reasons why content producers would be interested in video decentralization

1. People like free, and decentralization here happens to mean costs of distrubtion fall to zero as your users take on the burden of sharing the video with each other, seemlessly in the background while they watch the video.
2. Decentralized video is impossible to censor immediatly, and resistant to censorship over the long term.

Centralized internets systems are vulnerable to censorship. The aims of this project are to make the internet more decentralized for content. Using portable software that runs in a variaty of places, content can be generated which has built in redundancy. Instead of censoring one server in one location, now the gatekeepers have to censor perhapes 50 servers across the world in different jurisdictions.

Decentralization also shifts the burden of distribution video to the users themselves. This make the costs of distributing a video to anyone in the swarm effectively $0.

# How Video Swarm works

There are three components

1. There is the tracker server
2. There is the seeding servers
3. There is client code that the viewers automatically run when they visit your website,
  * They will consume the content
  * rebroadcast as seeders

There is also an additional component, a STUN server, but these are numerous and free. The clients will use a STUN server prior to joining a torrent swarm.

# Tracker Servers

This type of server manages the swarm. It allows viewers to quickly find peers that are ready to serve data, ue. who has downloaded what, and who is ready to serve what.

Clients will know how to connect to your tracker through the website that they visit.

The website will load javascript code `webtorrent.js` that will perform the necessary steps for the client contact this tracking server. Once the client has contacting the tracking the server, it will relay to the client, other clients that are eligable to serve the content to the clients.

<TODO> ADD WEBPAGE DEMO THAT GENERATES THE CORRECT IFRAME FROM A MAGNET URI </TODO>

Multiple tracker servers can exist for a piece of content.

The tracking server is packaged up in a docker instance, which can be deployed on Render.com free-tier of services.

For redundancy, multiple trackers should be used which will make the content impossible to censor.

#### Tracker Installation Instructions

  * Login to Render.com
  * Click the dashboard button
  * Click new -> Web Service
  * Connect Repository: `zackees/docker-bittorrent-tracker`
    * Give it a name
    * Use the free 512mb ram, shared CPU version
    * click create web service

When the app comes online you'll get the URL to the active tracking server.

#### Testing your Tracker

	* Go to https://webtorrentseeder.com
	* Modify the tracking url to use the yours.
	* upload content
	* copy the resulting magnet link
	* open up webtorrentseeder.com in a new window (not a tab!)
	* paste in the magnet link
	* check that the video transfers from one window to another


#### Tracking servers are embedded into the content urls

A tracking server will be linked with content by the magnet url that represents the content. The magnet url is a big url that includes tracking servers that promise to serve the content represented by the embedded cryptographic hash. So when a magnet url is passed around, the link to the tracking server goes with it. This allows the client information on who to contact (your tracking server) to get the file stream.

# Seeders

Seeders are like the spark plug to an ignition system. They provide the initial download sources for an incoming swarm, and maintain the swarm after the surge of interest leaves. As long as at least one seeder is connected to the swarm, the swarm is considered "healthy".

It's recommended that multiple seeders are used with a tracker to initiate the swarm. This can be one over the internet like this:

  * Go to webtorrentseeder.com
  * Put in the tracker, upload the file
  * Get the magnet link
  * Tear the browser tab out into it's own seperate window and keep it there
    * If you don't do this, then the uploading will be suspended whenever a different tab is selected.
  * KEEP THE BROWSER WINDOW OPEN!
  * Pass the magnet link around to friends / coworkers, have them
    * goto webtorrentseeder.com
    * enter in the magnet link
    * they will upgrade to seeders when they download the content.

Python way

This is a great way to get a seeder up and running. Run this on your own computer or spin up a cheap virtual private computer from digitalOcean ($5 / month) and then login.

Let's install the python command `webtorrent-seeder`

  * Make sure that python and pip are installed on your system.
  * `pip3 install webtorrent-seeder`
  * Now seed any file:
    * `webtorrent_seeder myfile.mp4` and follow the prompts.
      * if you want to use your own tracker (recommended) then use `webtorrent_seeder myfile.mp4 --trackers wss://mytracker.com:80`
    * Record the output magnet link
  * Verify the seeding worked by viewing the video at `webtorrentseeder.com` and pasting in the magnet url

# STUN servers

These are required servers that tell clients information necessary for them to connect to the swarm. The costs to run a STUN server is practically nothing so there are lots of STUN servers out there that can be used. There are literally hundreds out there and there are certain lists that exist on github that are updated every 30 mins. The stun servers will be part of the rtcConfig of the webtorrent client, which will contain a STUN server list of one or more urls.

# TURN Servers

We don't use TURN servers because this type of bandwidth turns out to be very expensive. If webtorrent doesn't work on a particular client then this should be handled at the application layer. Falling back to a file hosted on a CDN has known costs at about $0.01 per GB and this is going to be way cheaper than any bandwidth going in and out of a TURN server that you're hosting somewhere.

# Further work

## Bring in all the users

Not everyone can join the swarm right now. That includes all users with "Symetric NATs", which are common with cell phones connections.

Apparently some progress has been made that allows users hole punching under all conditions.

## Allow clients to contribute their bandwidth to the networks

Seeder bots could be used to provide boosted ignition bandwidth at the beginning of a new file. Such bots would monitor a data url which contains a list of magnet urls. When the magnet urls are updated, the seeder bots will detect this and begin preloading the video. When the video link is posted publically, the seeders have already buffered the video enough to provide the burst of bandwidth.
