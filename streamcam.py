from pathlib import Path

import ffmpeg

from settings import VideoSettings

video_settings = VideoSettings()

# Set up the video source and a fake audio source.
video_in = ffmpeg.input('/dev/video0', s=video_settings.video_size,
                        framerate=video_settings.framerate,
                        thread_queue_size=video_settings.thread_queue_size)
audio_in = ffmpeg.input('anullsrc', format='lavfi')

# Filter the frames with a simple two-frame time-blend.
# TODO pull from settings.
if video_settings.tblend:
    video_in = video_in.filter('chromanr')
    video_in = video_in.filter('tblend', all_mode='average')
    video_in = video_in.filter('zmq')

# Add the text from the banner and the time.
with video_settings.banner_path.open('w') as f:
    if video_settings.debug:
        f.write(video_settings.json(indent=2, exclude={'stream_key'}))
    else:
        f.write('Project PANOPTES MLO Streamcam')

video_in = video_in.drawtext(textfile=video_settings.banner_path.as_posix(),
                             reload=True,
                             **video_settings.font_styles.dict(),
                             y='h-10-text_h')
video_in = video_in.drawtext(textfile=video_settings.time_path.as_posix(),
                             reload=True,
                             **video_settings.font_styles.dict(),
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
