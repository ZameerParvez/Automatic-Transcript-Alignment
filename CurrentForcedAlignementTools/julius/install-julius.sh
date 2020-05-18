#!/bin/bash

LINE="=============================================================="

SOURCE=https://github.com/julius-speech/julius.git
MODEL_NAME=ENVR-v5.4.Dnn.Bin
MODEL_SOURCE=https://netix.dl.sourceforge.net/project/juliusmodels/"$MODEL_NAME".zip
ZIP_NAME=zipped
CONFIG_NAME=editted-dnn.jconf

apt-get install -y build-essential zlib1g-dev libsdl2-dev libasound2-dev git python2.7 python-pip python-wxtools python-wxgtk-media3.0
git clone "$SOURCE"
cd julius
./configure --enable-words-int
make -j4
# ls -l julius/julius
make install

cd ../
curl -o "$ZIP_NAME" "$MODEL_SOURCE"

unzip "$ZIP_NAME"
cp "$CONFIG_NAME" "$MODEL_NAME"/dnn.jconf
cd "$MODEL_NAME"