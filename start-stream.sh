#!/usr/bin/env bash

# Clears video buffer message.
modprobe -v -r uvcvideo && modprobe -v uvcvideo

/home/panoptes/mambaforge/bin/python3 streamcam.py stream
