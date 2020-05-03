# Gentle

## Introduction
Gentle is a force aligner built using the kaldi ASR toolkit.
It is one of the more convenient to use force aligners becuase the creators host a docker image which contains a server with the tool running as a web application.

## Docker
The docker image is provided by the creators of gentle at lowerquality/gentle. The docker-gentle.sh script I have provided just wraps it and exposes the containers server on port 8080 on the host machine.

```
This is a simple wrapper script to run gentle on port 8080 of the host machine. The docker image is pulled from lowerquality/gentle

To run, use:
    ./docker-gentle.sh -r

-h  --help      print this help message
-r  --run       run the container, if a container named gentle already exists then it will run that
-d  --destroy   prunes all unused images and containers
```

## How To Use
Once the container is running, you can either send messages to the server by rpc, or go to https://localhost:8080 and interface with it from there.

Alternatively it can be run from the command line, if you have the source, or with curl.

```
curl -F "audio=@Audio.mp3" -F "transcript=@transcript.txt" "http://localhost:8080/transcriptions?async=false"

# with the source this is used
python3 align.py Audio.mp3 transcript.txt
```

They also have a web app available to test with http://gentle-demo.lowerquality.com/

## References
https://github.com/lowerquality/gentle