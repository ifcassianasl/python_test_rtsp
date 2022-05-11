from flask import Flask
import ffmpeg_streaming
from ffmpeg_streaming import Formats

import sys

app = Flask(__name__)

@app.route("/")
def streaming():
  video = ffmpeg_streaming.input('rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4')

  hls = video.hls(Formats.h264())
  hls.auto_generate_representations()
  return hls.output('/var/media/hls.m3u8', monitor=monitor)

def monitor(ffmpeg, duration, time_, time_left, process):
  per = round(time_ / duration * 100)
  sys.stdout.write(
    "\rTranscoding...(%s%%) %s left [%s%s]" %
    (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
  )
  sys.stdout.flush()