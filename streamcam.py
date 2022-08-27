import os
import ffmpeg
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()

stream_key = os.environ['STREAM_KEY']
stream_url = f'rtmp://a.rtmp.youtube.com/live2/{stream_key}'
print(f'Starting stream on {stream_url}')

video_in = (
    ffmpeg.input('/dev/video0', framerate=24, video_size='uhd2160')
    .filter('drawtext', text='Project PANOPTES MLO Streamcam', x='w-text_w-10', y='h-text_h-10', color='yellow', font='mono')
    .output(stream_url, format='flv')
)