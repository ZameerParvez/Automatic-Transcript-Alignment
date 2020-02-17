# Gentle

## Introduction
Gentle is a force aligner built using the kaldi ASR toolkit.
It is one of the more convinient to use force aligners becuase the creators host a docker image which contains a server with the tool running as a web application.

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

Alternativley it can be run from the command line, if you have the source, or with curl.

```
curl -F "Audio.mp3" -F "transcript.txt" "http://localhost:8080/transcriptions?async=false"

python3 align.py Audio.mp3 transcript.txt
```

They also have a web app available to test with http://gentle-demo.lowerquality.com/

## References
https://github.com/lowerquality/gentle


## Comments
- The output foramt is a json
- Uses kaldis modern network and has many easy ways to use it, and has permissive liscensing
- I think a lot of the work it does is accomodate different inputs and complete the aligning with sequence alignment
    - need to check this though

- Processes significantly slower than aeneas, and requires more resources
- The transcript is a lot more accurate than aeneas, and is at the phoneme level
- It also has a very nice UI for baing able to play back the audio with the alignement, and seek to where the word is said
- The GUI is very simple and there aren.t many options so it is much easier to use

- This uses an acoustic model trained by kaldi developers on the Fisher English corpus
    - This means it is closely tied to the language
        - It won't be easy to produce a good model like that for other languages
    
- The sequence alignment may also be language dependant