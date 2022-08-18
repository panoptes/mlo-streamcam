#!/usr/bin/env bash

STREAM_KEY=...

# Clears video buffer message.
sudo modprobe -v -r uvcvideo && sudo modprobe -v uvcvideo

# For text options see:
# https://stackoverflow.com/questions/17623676/text-on-video-ffmpeg

ffmpeg \
    -f lavfi -i anullsrc -acodec aac \
    -thread_queue_size 128 \
    -s 3840x2160 \
    -i /dev/video0 \
    -vf "drawtext=textfile=time.txt:reload=1:fontcolor=yellow:fontsize=36:box=1:boxcolor=black@0.5:boxborderw=5:x=w-text_w-10:y=(h-text_h)-10,drawtext=textfile=banner.txt:reload=1:fontcolor=yellow:fontsize=36:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=(h-text_h)-10" \
    -vcodec libx264 \
    -pix_fmt yuv422p \
    -s 3840x2160 \
    -preset ultrafast \
    -r 30 -g 60 \
    -bufsize 4M -maxrate 25M \
    -f flv "rtmp://a.rtmp.youtube.com/live2/${STREAM_KEY}"