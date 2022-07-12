// What NAT am I using?
// https://clients.dh2i.com/NatTest/

const WebTorrent = require('webtorrent')
var prompt = require('prompt');
const client = new WebTorrent()

function doSeed(trackers, files) {
    console.log("Seeding: ", files, " with trackers", trackers)
    client.seed(files, { announce: trackers }, torrent => {
        console.log(`Seeded: ${torrent.name}\nmagnetURI: ${torrent.magnetURI}`)
    })
    client.on("error", err => {
        console.error(err)
    });
}

prompt.start()
prompt.get(['tracker', 'file'], function (err, result) {
    result.file = result.file || './test.mp4'
    result.tracker = result.tracker || 'wss://tracker.btorrent.xyz'
    const FILES = [result.file]
    doSeed([result.tracker], FILES)
});
