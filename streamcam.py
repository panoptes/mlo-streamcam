from pathlib import Path

import ffmpeg

from settings import VideoSettings

banner_path = Path('banner.txt')
time_path = Path('time.txt')

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
# TODO pull from env var.
video_in_split = video_in.filter('tblend', all_mode='average').filter_multi_output('split')
video_in = video_in_split[0]

if video_settings.show_zoom:
    video_in_overlay = video_in_split[1].crop(x=f'iw/{video_settings.crop_scale}',
                                              y=f'ih/{video_settings.crop_scale}',
                                              width=f'iw/{video_settings.crop_scale}',
                                              height=f'ih/{video_settings.crop_scale}')

    video_in = video_in.overlay(video_in_overlay, x=10, y=10)

# Add the text from the banner and the time.
with banner_path.open('w') as f:
    if video_settings.debug:
        f.write(video_settings.json(indent=2, exclude={'stream_key'}))
    else:
        f.write('Project PANOPTES MLO Streamcam')

video_in = video_in.drawtext(textfile=banner_path.as_posix(),
                             reload=True,
                             **font_styles,
                             y='h-10-text_h')
video_in = video_in.drawtext(textfile=time_path.as_posix(),
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
                       bufsize=video_settings.buf_size,
                       maxrate=video_settings.max_rate
                       )

output.run()
