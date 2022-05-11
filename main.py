from flask import Flask
from flask import render_template
import ffmpeg_streaming
from ffmpeg_streaming import Formats

import sys

app = Flask(__name__)

@app.route("/")
def streaming():
  return render_template('streaming.html')

@app.route('/video')
def video_server():
  video = ffmpeg_streaming.input('pexels_video.mp4')

  hls = video.hls(Formats.h264())
  hls.auto_generate_representations()
  hls.save_master_playlist('/var/media/hls.m3u8')

  return hls.output('/var/media/hls.m3u8')

def monitor(ffmpeg, duration, time_, time_left, process):
  per = round(time_ / duration * 100)
  sys.stdout.write(
    "\rTranscoding...(%s%%) %s left [%s%s]" %
    (per, datetime.timedelta(seconds=int(time_left)), '#' * per, '-' * (100 - per))
  )
  sys.stdout.flush()