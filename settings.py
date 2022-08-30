from pathlib import Path

from pydantic import BaseSettings, BaseModel


class TextStyle(BaseModel):
    fontcolor: str = 'yellow'
    fontsize: int = 36
    box: int = 1
    boxcolor: str = 'black@0.5'
    boxborderw: int = 5


class VideoSettings(BaseSettings):
    """Settings for youtube streaming."""
    stream_key: str = None
    crf: int = 20
    preset: str = 'superfast'
    framerate: int = 25
    keyframerate: int = 25
    filters: str = 'tmix=frames=3:weights=1 1 1'
    # n.b. ffmpeg-python does not support named sized, e.g. uhd2160.
    video_size: str = '3840x2160'
    buf_size: str | int = '5M'
    max_rate: str | int = '40M'
    thread_queue_size: int = 512
    debug: bool = False

    banner_path: Path = Path('banner.txt')
    time_path: Path = Path('time.txt')

    font_styles: TextStyle = TextStyle()

    @property
    def stream_url(self):
        return f'rtmp://a.rtmp.youtube.com/live2/{self.stream_key}'

    class Config:
        env_file = '.env'
