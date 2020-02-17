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

## Comments

- Inputs have to be formatted correctly
    - For the transcript, the fragment delimiting depeds on the format of the text. https://www.readbeyond.it/aeneas/docs/clitutorial.html#input-text-formats
    - For the audio mp3 is prefferred, but I think it works as long as ffmpeg is able to decode it
        - It works with sph.

- Supports many different output formats including srt
    - Other formats are used for different purposed
        - captioning
        - research
        - digital publishing
        - web
        - further prosessing

- Uses fairly modern hardware and also has a test suite
    - e.g. 64 bit machine + OS with more than 4gb ram

- There is also a vagrant config which has it already set up in a VM
    - This makes it easier for more people to get it running, because it is a consistent environment

- It is installed with pip, so it is run as a python module
    - To improve performance it also has C extensions
    - This is also good because it retains the useability of python and the performance of C
        - MFCC and DTW are the specific parts done with C to improve performance

- The quality of the alignement is not great
    - The first fragment starts at 0 but should start at 13
        - So the subtitles would appear before they are said, during the opening music
            - This may indicate that it doesnt work well with music or not starting on speech straight away
            - There is a similar situation with the last fragment
    - There is a reasonable difference in the order of seconds between the given alignement of TEDlium (which is fairly accurate) and the srt produced when I ran it
        - There are a few potential causes for this
            - poor parameter choices
            - poorly formatted transcript
            - using an older TTS engine

- The biggest advantage of this solution over others is the weaker dependency on languages, because the language is only used for TTS
    - This means that it should work as long as a good TTS exists for the language
    - No language models are needed, which are more difficult to aquire compared to TTS engines

- technology used....
    - The general process is
        - pre process audio so that it is in a mono wave format
        - Synthesize mono waves from the text using TTS and generate a text to synt time map
            - A synt has some meaning in linguistics ....................
            - The TTS is the only part of the process which is dependant on the language
                - This makes it a more flexible method than ASR based methods
        - 