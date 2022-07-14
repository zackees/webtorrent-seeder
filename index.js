// What NAT am I using?
// https://clients.dh2i.com/NatTest/

const WebTorrent = require('webtorrent')
const prompt = require('prompt')

const DEFAULT_TRACKER = 'wss://webtorrent-tracker.onrender.com:80'

const WEBTORRENT_CONFIG = {
  tracker: {
    rtcConfig: {
      iceServers: [
        {
          urls: [
            'stun:stun.l.google.com:19302',
            'stun:stun1.l.google.com:19302',
            'stun:stun2.l.google.com:19302',
            'stun:global.stun.twilio.com:3478'
          ]
        }
      ],
      sdpSemantics: 'unified-plan',
      bundlePolicy: 'max-bundle',
      iceCandidatePoolsize: 1
    }
  }
}

if (!WebTorrent.WEBRTC_SUPPORT) {
  console.error('This browser is unsupported. Please use a browser with WebRTC support.')
}

const webtorrentClient = new WebTorrent(WEBTORRENT_CONFIG)

function doSeed (trackers, files) {
  console.log('Seeding: ', files, ' with trackers', trackers)
  webtorrentClient.seed(files, { announce: trackers }, torrent => {
    console.log(`Seeded: ${torrent.name}\nmagnetURI: ${torrent.magnetURI}`)
  })
  webtorrentClient.on('error', err => {
    console.error(err)
  })
}

prompt.start()
prompt.get(['tracker', 'file'], function (err, result) {
  if (err) {
    console.error(err)
  } else {
    result.file = result.file || './test.mp4'
    result.tracker = result.tracker || DEFAULT_TRACKER
    const FILES = [result.file]
    doSeed([result.tracker], FILES)
  }
})

