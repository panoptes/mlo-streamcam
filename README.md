# mlo-streamcam
Software and resources for the MLO streaming video camera system.

## Streaming

The video stream is being done by `ffmpeg` in the [`start-stream.sh`](start-stream.sh) script.

The script overlays two text files onto the video, the `banner.txt` in the lower left corner and the `time.txt` in the lower right.

The `banner.txt` file can be updated manually and will update in the video as soon as the file is saved. 

The `time.txt` file is updated automatically by the [`get-updates.py`](get-updates.py) script.

Both [`get-updates.py`](get-updates.py) and [`start-stream.sh`](start-stream.sh) are controlled by supervisord via the [`supervisord.conf`](supervisord.conf), which should be symlinked into the main configuration directory:

```bash
sudo ln -s $PWD/supervisord.conf /etc/supervisor/conf.d/
```

## pico-controller

The pico controls the relays and reads the temperature from inside the camera box.

The [`get-updates.py`](get-updates.py) script reads the output from [`pico-controller/main.py`](pico-controller/main.py) over the serial line and stores it in a file called `pico-log.json`.

See the [README](pico-controller/README.md).

## Requirements

The `get-updates.py` script requires the `panoptes-utils` module to be installed:

```bash
pip install panoptes-utils
```

To use the [`supervisord.conf`](supervisord.conf) you must have [`supervisor`](http://supervisord.org/) installed:

```bash
sudo apt-get install supervisor
```
