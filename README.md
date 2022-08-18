# mlo-streamcam
Software and resources for the MLO streaming video camera system.


## Streaming

The video stream is being done by `ffmpeg` in the [`start-stream.sh`](start-stream.sh) script.

The script overlays two text files onto the video, the `banner.txt` in the lower left corner and the `time.txt` in the lower right.

The `banner.txt` file can be updated manually and will update in the video as soon as the file is saved. 

The `time.txt` file is updated automatically by the [`get-updates.py`](get-updates.py) script.

## pico-controller

The pico controls the relays and reads the temperature from inside the camera box.

See the [README](pico-controller/README.md).