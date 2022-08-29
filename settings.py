from pydantic import BaseSettings


class VideoSettings(BaseSettings):
    """Settings for youtube streaming."""
    stream_key: str = None
    crf: int = 20
    preset: str = 'superfast'
    framerate: int = 25
    keyframerate: int = 25
    # n.b. ffmpeg-python does not support named sized, e.g. uhd2160.
    video_size: str = '3840x2160'
    buf_size: str | int = '5M'
    max_rate: str | int = '40M'
    thread_queue_size: int = 512
    show_zoom: bool = False
    tblend: bool = False
    debug: bool = False

    @property
    def stream_url(self):
        return f'rtmp://a.rtmp.youtube.com/live2/{self.stream_key}'

    class Config:
        env_file = '.env'