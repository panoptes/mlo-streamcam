import ffmpeg
from pydantic import BaseSettings


class VideoSettings(BaseSettings):
    """Settings for youtube streaming."""
    stream_key: str
    crf: int = 20
    preset: str = 'ultrafast'
    framerate: int = 30
    keyframerate: int = 60
    # n.b. ffmpeg-python does not support named sized, e.g. uhd2160.
    video_size: str = '3840x2160'
    bufsize: str | int = '5M'
    maxrate: str | int = '40M'
    thread_queue_size: int = 512

    @property
    def stream_url(self):
        return f'rtmp://a.rtmp.youtube.com/live2/{self.stream_key}'

    class Config:
        env_prefix = 'pocs_'


font_styles = dict(
    fontcolor='yellow',
    fontsize=36,
    box=1,
    boxcolor='black@0.5',
    boxborderw=5,
)

video_settings = VideoSettings()

# Set up the video source and a fake audio source.
video_in = ffmpeg.input('/dev/video0', s=video_settings.video_size,
                        framerate=video_settings.framerate,
                        thread_queue_size=video_settings.thread_queue_size)
audio_in = ffmpeg.input('anullsrc', format='lavfi')

# Filter the frames with a simple two-frame time-blend.
video_in = video_in.filter('tblend', all_mode='average')

# Add the text from the banner and the time.
video_in = video_in.drawtext(textfile='banner.txt',
                             reload=True,
                             **font_styles,
                             y='h-10-text_h')
video_in = video_in.drawtext(textfile='time.txt',
                             reload=True,
                             **font_styles,
                             x='w-10-text_w',
                             y='h-10-text_h')

output = ffmpeg.output(audio_in,
                       video_in,
                       video_settings.stream_url,
                       format='flv',
                       vcodec='libx264',
                       crf=video_settings.crf,
                       preset=video_settings.preset,
                       r=video_settings.framerate,
                       g=video_settings.keyframerate,
                       s=video_settings.video_size,
                       bufsize=video_settings.bufsize,
                       maxrate=video_settings.maxrate
                       )

output.run()
