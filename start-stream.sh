#!/usr/bin/env bash

# Source .env file in directory.
set -o allexport; source .env; set +o allexport

STREAM_KEY="${STREAM_KEY:-ENTER STREAM KEY}"
FRAMERATE=${FRAMERATE:-30}
KEYFRAMERATE=${KEYFRAMERATE:-30}  # in fps
VIDEO_SIZE=${VIDEO_SIZE:-4k}
BUFFER_SIZE=${BUFFER_SIZE:-4M}
MAX_RATE=${MAX_RATE:-20M}

# Clears video buffer message.
modprobe -v -r uvcvideo && modprobe -v uvcvideo

# For text options see:
# https://stackoverflow.com/questions/17623676/text-on-video-ffmpeg

ffmpeg \
    -f lavfi -i anullsrc -acodec aac \
    -f v4l2 \
    -thread_queue_size 128 \
    -framerate "${FRAMERATE}" \
    -video_size "${VIDEO_SIZE}" \
    -i /dev/video0 \
    -vf "drawtext=textfile=time.txt:reload=1:fontcolor=yellow:fontsize=36:box=1:boxcolor=black@0.5:boxborderw=5:x=w-text_w-10:y=(h-text_h)-10,drawtext=textfile=banner.txt:reload=1:fontcolor=yellow:fontsize=36:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=(h-text_h)-10" \
    -vcodec libx264 \
    -pix_fmt yuv422p \
    -s "${VIDEO_SIZE}" \
    -preset ultrafast \
    -r "${FRAMERATE}" \
    -g "${KEYFRAMERATE}" \
    -bufsize "${BUFFER_SIZE}" \
    -maxrate "${MAX_RATE}" \
    -f flv "rtmp://a.rtmp.youtube.com/live2/${STREAM_KEY}"