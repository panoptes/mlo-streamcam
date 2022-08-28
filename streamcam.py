import os
import ffmpeg
from datetime import datetime as dt
from dotenv import load_dotenv

load_dotenv()

stream_key = os.environ['STREAM_KEY']
stream_url = f'rtmp://a.rtmp.youtube.com/live2/{stream_key}'

crf=os.getenv('CRF', 20)
preset=os.getenv('PRESET', 'ultrafast')
framerate=os.getenv('FRAMERATE', 30)
keyframerate=os.getenv('KEYFRAMERATE', 30)
# n.b. ffmpeg-python does not support named sized, e.g. uhd2160.
video_size=os.getenv('VIDEO_SIZE', '3840x2160')
bufsize=os.getenv('BUFSIZE', '5M')
maxrate=os.getenv('MAXRATE', '40M')

print(f'Starting stream on {stream_url}')

font_styles = dict(
    fontcolor='yellow',
    fontsize=36,
    box=1,
    boxcolor='black@0.5',
    boxborderw=5,
)

# Set up the video source and a fake audio source.
video_in = ffmpeg.input('/dev/video0', s='3840x2160', framerate=30, thread_queue_size=512)
audio_in = ffmpeg.input('anullsrc', format='lavfi')

# Filter the frames with a simple two-frame time-blend.
video_in = video_in.filter('tblend', all_mode='average')

# Add the text from the banner and the time.
video_in = video_in.drawtext(textfile='banner.txt', reload=True, **font_styles, y='h-10-text_h')
video_in = video_in.drawtext(textfile='time.txt', reload=True, **font_styles, x='w-10-text_w', y='h-10-text_h')

output = ffmpeg.output(audio_in, 
                        video_in, 
                        stream_url, 
                        format='flv', 
                        vcodec='libx264', 
                        crf=crf, 
                        preset=preset, 
                        r=framerate, 
                        g=keyframerate, 
                        s=video_size, 
                        bufsize=bufsize, 
                        maxrate=maxrate
                        )

output.run()