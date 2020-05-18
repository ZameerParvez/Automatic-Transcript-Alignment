# Aeneas

## Introduction
Aeneas is a force alignement tool designed to align at the fragment level, although it can be used to produce a more fine grained alignment.

## Install Procedure
To install aeneas run the install-aeneas.sh script.

## Docker
The dockerfile here can make a container with aeneas installed.

```
This script helps with building the docker image and running the container interactively, you could alternativley use docker commands.

To build and run, use:
    ./docker-aeneas.sh -b
    ./docker-aeneas.sh -r

This will also create an aeneas folder in the current directory which is where the volume is on the host machine.00:18:04,760 --> 00:18:28,280


-h  --help      print this help message
-b  --build     build the docker image
-r  --run       run the container, if a container named aeneas already exists then it will run that
-v  --volume    can specify a volume to use for the docker image, by default it will be <current directory>/aeneas and will be mounted at /working-folder in the container (This can only be specified on the first run of the container)
-d  --destroy   prunes all unused images and containers
```

## How To Use
Once in the docker container or once aeneas is installed you can use aeneas like it would be run locally,which involves executing a task.

The tasks that aeneas works on are triples of audio file, transcript and configuration parameters.

These tasks can be batch processed as jobs.

```
python -m aeneas.tools.execute_job

python -m aeneas.tools.execute_task

python -m aeneas.tools.execute_task AUDIO_FILE  TEXT_FILE CONFIG_STRING OUTPUT_FILE [OPTIONS]

aeneas_execute_task AUDIO_FILE  TEXT_FILE CONFIG_STRING OUTPUT_FILE [OPTIONS]
```

An example given in the documentation to create an srt would set the config string to "task_language=eng|is_text_type=subtitles|os_task_file_format=srt". So a complete example that would output an SRT file would look like:
```
python -m aeneas.tools.execute_task audio.mp3 transcript.txt "task_language=eng|is_text_type=subtitles|os_task_file_format=srt" subtitle.srt

aeneas_execute_task audio.mp3 transcript.txt "task_language=eng|is_text_type=subtitles|os_task_file_format=srt" subtitle.srt
```


A much easier way to use aeneas is through it's web app, although an account is required.

Aeaneas web app: https://aeneasweb.org

Aeneas Docs: https://www.readbeyond.it/aeneas/docs/index.html

## References

https://github.com/readbeyond/aeneas