#!/usr/bin/env bash

# Source .env file in directory.
set -o allexport; source .env; set +o allexport

STREAM_KEY="${STREAM_KEY:-ENTER STREAM KEY}"
CRF=${CRF:-18}
FRAMERATE=${FRAMERATE:-30}
KEYFRAMERATE=${KEYFRAMERATE:-30}  # in fps
VIDEO_SIZE=${VIDEO_SIZE:-uhd2160}
BUFFER_SIZE=${BUFFER_SIZE:-4M}
MAX_RATE=${MAX_RATE:-20M}
PRESET=${PRESET:-faster}
BSFILTERS=${BSFILTERS:-tmix=6}

DEBUG=${DEBUG:-false}

# For text options see:
# https://stackoverflow.com/questions/17623676/text-on-video-ffmpeg
TEXT_STYLE="fontcolor=yellow:fontsize=36:box=1:boxcolor=black@0.5:boxborderw=5"
POSITION_BL="x=10:y=h-(text_h+10)"
POSITION_BR="x=w-(text_w+10):y=h-(text_h+10)"
BANNER_TEXT="drawtext=textfile=banner.txt:reload=1:${TEXT_STYLE}:${POSITION_BL}"
TIME_TEXT="drawtext=textfile=time.txt:reload=1:${TEXT_STYLE}:${POSITION_BR}"

# Clears video buffer message.
modprobe -v -r uvcvideo && modprobe -v uvcvideo

if [ "$DEBUG" == true ]; then
    # Update the banner text to show the settings except key.
    cat .env | grep -v STREAM_KEY > banner.txt
else 
    echo "Project PANOPTES" > banner.txt
fi

ffmpeg \
    -f lavfi -i anullsrc -acodec aac \
    -f v4l2 \
    -thread_queue_size 512 \
    -framerate "${FRAMERATE}" \
    -video_size "${VIDEO_SIZE}" \
    -i /dev/video0 \
    -vf "${BSFILTERS},${TIME_TEXT},${BANNER_TEXT}" \
    -vcodec libx264 \
    -pix_fmt yuv422p \
    -s "${VIDEO_SIZE}" \
    -preset "${PRESET}" \
    -r "${FRAMERATE}" \
    -g "${KEYFRAMERATE}" \
    -crf "${CRF}" \
    -bufsize "${BUFFER_SIZE}" \
    -maxrate "${MAX_RATE}" \
    -f flv "rtmp://a.rtmp.youtube.com/live2/${STREAM_KEY}"
