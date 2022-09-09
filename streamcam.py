#!/usr/bin/env python3

import time
from datetime import datetime as dt
from pathlib import Path

import ffmpeg
import typer
from panoptes.utils.serial.device import SerialDevice
from panoptes.utils.serializers import from_json, to_json

from settings import VideoSettings

app = typer.Typer()


@app.command('debug')
def show_debug(turn_off: bool = False):
    """Command to control the debug info."""
    video_settings = VideoSettings()
    with video_settings.banner_path.open('w') as f:
        if turn_off:
            f.write('Project PANOPTES MLO Streamcam')
        else:
            f.write(video_settings.json(indent=2, exclude={'stream_key'}))


@app.command('stream')
def stream_video(dry_run: bool = False):
    """Stream the video camera to YouTube."""
    # Get the video settings. This will load the .env file.
    video_settings = VideoSettings()

    if video_settings.stream_key is None and dry_run is False:
        typer.secho('No stream key set. Please set the STREAM_KEY environment variable.',
                    fg=typer.colors.RED)
        return

    # Set up the video source and a fake audio source.
    video_in = ffmpeg.input(video_settings.device,
                            s=video_settings.video_size,
                            framerate=video_settings.framerate,
                            thread_queue_size=video_settings.thread_queue_size)
    audio_in = ffmpeg.input('anullsrc', format='lavfi')

    # Set up the video filters.
    if video_settings.filters > '':
        for filter_name, filter_kwargs in parse_filters(video_settings.filters):
            video_in = video_in.filter(filter_name, **filter_kwargs)

        # Add in zmq filter for command control.
        video_in = video_in.filter('zmq')

    # Turn on or off the debug info.
    show_debug(video_settings.debug)

    # Show a zoomed in view of an area of the image.
    if video_settings.zoom_box is not None:
        x, y, w, h = video_settings.zoom_box.split(',')
        video_in_split = video_in.filter_multi_output('split')
        video_in_overlay = video_in_split[1].crop(x=x, y=y, width=w, height=h)

        video_in = video_in_split[0].overlay(
            video_in_overlay.filter('scale', width='400', height='400'), x=10, y=10)
        # Show the box on the original
        video_in = video_in.drawbox(x, y, w, h, color='red', thickness=3)

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

    # Run (or just show) the command.
    if dry_run:
        typer.secho(output.compile(), fg=typer.colors.BLUE)
        if video_settings.stream_key is None:
            typer.secho('Showing None instead of stream key in above URL.', fg=typer.colors.RED)
    else:
        output.run()


@app.command('monitor')
def monitor_environment(port: str = '/dev/ttyACM0',
                        time_path: Path = VideoSettings().time_path,
                        log_path: Path = VideoSettings().log_path,
                        ):
    """Monitors the video camera environment.

    This records the serial data from the pico controller, updates the time, and
    may record other metadata.
    """
    device = SerialDevice(port=port, reader_callback=from_json)

    while True:
        with time_path.open('w') as f0, log_path.open('a') as f1:
            try:
                # Get the temperature
                temp_c = device.readings[-1]["temp_c"]

                # Write to the time.txt file, include the temperature.
                f0.write(f'{dt.now():%c} HST {temp_c:10.01f}° C')

                # Write the readings.
                f1.write(to_json(dict(time=dt.now().isoformat(), temp_c=temp_c)))
                f1.write('\n')
            except Exception as e:
                print(e)

        time.sleep(1)


def parse_filters(filters_string):
    """Parse a filter string into a list of ffmpeg filters.

    Given a string of ffmpeg filters, e.g. 'tmix=frames=3:weights=1 1 1',
    yield the name of the filter and a dictionary of the arguments, i.e.
    ('tmix', {'frames': '3', 'weights': '1 1 1'}).
    """
    for filter_str in filters_string.split(','):
        filter_name, filter_args = filter_str.split('=', 1)
        yield filter_name, dict(arg.split('=') for arg in filter_args.split(':'))


if __name__ == '__main__':
    app()
