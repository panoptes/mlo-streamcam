from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class TextStyle(BaseModel):
    fontcolor: str = 'yellow'
    fontsize: int = 24
    font: str = 'mono'
    box: int = 1
    boxcolor: str = 'black@0.5'
    boxborderw: int = 5


class VideoSettings(BaseSettings):
    """Settings for YouTube streaming."""
    stream_key: str | None = None
    device: str = '/dev/video0'
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
    zoom_box: str | None = None  # 'x,y,w,w e.g. (iw/2-50),(iw/2-50),100,100'

    banner_path: Path = Path('banner.txt')
    time_path: Path = Path('time.txt')
    log_path: Path = Path('pico-log.json')

    font_styles: TextStyle = TextStyle()

    @property
    def stream_url(self):
        return f'rtmp://a.rtmp.youtube.com/live2/{self.stream_key}'

    class Config:
        env_file = '.env'
