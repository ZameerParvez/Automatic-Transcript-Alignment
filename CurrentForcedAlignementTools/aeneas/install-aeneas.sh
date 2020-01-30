#!/bin/bash

LINE="=============================================================="

echo "$LINE"
echo "Installing dependencies"
apt-get install -y \
    build-essential flac libasound2-dev libsndfile1-dev vorbis-tools libxml2-dev libxslt-dev zlib1g-dev \
    python-dev python-pip ffmpeg make espeak espeak-data libespeak1 libespeak-dev festival*

pip install numpy beautifulsoup4 lxml setuptools
echo "$LINE"

echo "$LINE"
echo "Installing Aeneas"
pip install aeneas
echo "$LINE"