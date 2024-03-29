# mlo-streamcam

Software and resources for the MLO streaming video camera system.

## Overview

The MLO streaming video camera system is a collection of software and hardware
used to stream a near real-time high-resolution (4k) video stream of the night
sky from the Mauna Loa Observatory (MLO) in Hawaii to YouTube.

The system consists of a digital camera connected to the computer via a [Magewell
capture card](https://www.magewell.com/products/usb-capture-hdmi-4k-plus) as well as a
[Raspberry Pi pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) that monitors the temperature near the
camera and can also control a relay to reset the camera when needed.

The code for the Raspberry Pi pico is in the `pico-controller` directory. See [pico-controller](#pico-controller) below
for more details.

The [`streamcam.py`](streamcam.py) script supports two sub-commands: `stream` and `monitor`.
The `stream` sub-command is used to start the streaming server. The `monitor` sub-command
is used to read the serial output from the [pico-controller/main.py](pico-controller/main.py) file.

Default parameters for both the commands can be specified in a `.env` file that should be created by the user. At a
minimum this should include the YouTube `STREAM_KEY` environment variable. See the [Settings](#settings)
section below for more details.

The system is controlled by [supervisord](http://supervisord.org/), which starts both the
`stream` and `monitor` commands at system boot.

The `stream` command is started via the [`start-streamcam.sh`](start-streamcam.sh) script in order to also unload and
reload the linux usb drivers.

## Installation

### Requirements

The [`requirements.txt`](requirements.txt) file contains the python requirements for the scripts.

```bash
pip install -r requirements.txt
```

To use the [`supervisord.conf`](supervisord.conf) you must have [`supervisor`](http://supervisord.org/) installed:

```bash
sudo apt-get install supervisor
```

The [`supervisord.conf`](supervisord.conf) provided in the repo will start both the `monitor` and `stream` commands and
should be symlinked into the main `supervisord` configuration directory:

```bash
sudo ln -s $PWD/streamcam-supervisord.conf /etc/supervisor/conf.d/
```

> Note: The `streamcam-supervisord.conf` file assumes your username is `panoptes` and your home directory is `/home/panoptes`. If this is different then alter the above file for your correct username and home directory.

## Settings

<a name="settings"></a>

The `streamcam` script has default settings contained in the [`settings.py`](settings.py) file. These can be
overridden by setting environment variables in a `.env` file that you create in the root directory of the repo.

The `.env` file should contain your YouTube `STREAM_KEY` as well as any other settings you want to override.

For example, to change the default framerate to 30 fps and buffer size to `2M`, create a `.env` file in the same
directory with the following contents:

```bash
STREAM_KEY=your-stream-key
FRAMERATE=30
BUF_SIZE=2M
```

See the [`settings.py`](settings.py) file for a list of all the available settings.

## Usage

### cli

You can run the program via the `streamcam.py` file, using the `stream` and `monitor` subcommands.

### streamcam stream

```py
python streamcam.py stream
```

The video stream is being done by `ffmpeg` via the [`ffmpeg-ptyhon`](https://github.com/kkroening/ffmpeg-python)
wrapper.

Options for ffmpeg are controlled via environment variables. See the [settings](#settings) section below.

The script overlays two text files onto the video, the `banner.txt` in the lower
left corner and the `time.txt` in the lower right.

The `banner.txt` file can be updated manually and will update in the video as soon as the file is saved. If the
environment variable `DEBUG=true` then the contents of `.env` (except the `STREAM_KEY`) will be displayed instead of the banner.

The `time.txt` file is updated automatically by the `monitor` sub-command.

### streamcam monitor

```py
python streamcam.py stream
```

The `monitor` sub-command reads the serial output from the [pico-controller/main.py](pico-controller/main.py) file and
stores it locally as `pico-log.json` text file. It also updates the `time.txt` file with the current time and the
current temperature.

### start-stream.sh

There is also a bash script that will unload and load the linux kernel module before starting the script, which can be 
helpful for freezing video.

Note that the bash script does assume the user is named `panoptes` and has a hard-coded python path. You may need to
adjust as necessary.


```bash
bash start-stream.sh
```

### supervisor

When running in automatic mode, the system is controlled by `supervisord`, which is responsible for running 
both the `stream` and the `monitor` described above. To control the system you should use `supervisorctl` instead 
of calling the scripts directly.

#### Restarting the service

If you need to manually restart the service call the below two commands:

```bash
sudo supervisorctl stop stream
sudo supervisorctl start stream
```

Note that it takes a few seconds for `stop stream` to kill all the `ffmpeg` processes and for some reason using `supervisorctl restart stream` doesn't wait, so the camera gets jammed.  Always use the explicit `stop/start`.

## pico-controller

The pico controls the relays and reads the temperature from inside the camera box.

See the [README](pico-controller/README.md).
