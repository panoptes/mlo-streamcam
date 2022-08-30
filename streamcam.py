import typer
import ffmpeg

from settings import VideoSettings


def parse_filters(filters_string):
    """Parse a filter string into a list of ffmpeg filters."""
    filters = {}
    for filter_str in filters_string.split(','):
        filter_name, filter_args = filter_str.split('=', 1)
        yield filter_name, dict(arg.split('=') for arg in filter_args.split(':'))


def main():
    # Get the video settings. This will load the .env file.
    video_settings = VideoSettings()

    if video_settings.stream_key is None:
        typer.secho('No stream key set. Please set the STREAM_KEY environment variable.',
                    fg=typer.colors.RED)
        return

    # Set up the video source and a fake audio source.
    video_in = ffmpeg.input('/dev/video0', s=video_settings.video_size,
                            framerate=video_settings.framerate,
                            thread_queue_size=video_settings.thread_queue_size)
    audio_in = ffmpeg.input('anullsrc', format='lavfi')

    if video_settings.filters > '':
        for filter_name, filter_kwargs in parse_filters(video_settings.filters):
            video_in = video_in.filter(filter_name, **filter_kwargs)

        # Add in zmq filter for command control.
        video_in = video_in.filter('zmq')

    # Add the text from the banner and the time.
    with video_settings.banner_path.open('w') as f:
        if video_settings.debug:
            f.write(video_settings.json(indent=2, exclude={'stream_key'}))
        else:
            f.write('Project PANOPTES MLO Streamcam')

    # Draw the text boxes.
    video_settings.banner_path.touch(exist_ok=True)
    video_in = video_in.drawtext(textfile=video_settings.banner_path.as_posix(),
                                 reload=True,
                                 **video_settings.font_styles.dict(),
                                 y='h-10-text_h')
    video_settings.time_path.touch(exist_ok=True)
    video_in = video_in.drawtext(textfile=video_settings.time_path.as_posix(),
                                 reload=True,
                                 **video_settings.font_styles.dict(),
                                 x='w-10-text_w',
                                 y='h-10-text_h')

    # Build the ffmpeg command.
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

    # Run the command.
    output.run()


if __name__ == '__main__':
    typer.run(main)
