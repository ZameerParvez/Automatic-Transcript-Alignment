#!/bin/bash
HELP=\
"
This script helps with building the docker image and running the container interactively, you could alternativley use docker commands.

To build and run, use:
    ./docker-aeneas.sh -b
    ./docker-aeneas.sh -r

This will also create an aeneas folder in the current directory which is where the volume is on the host machine.

-h  --help      print this help message
-b  --build     build the docker image
-r  --run       run the container, if a container named aeneas already exists then it will run that
-v  --volume    can specify a volume to use for the docker image, by default it will be <current directory>/aeneas and will be mounted at /working-folder in the container (This can only be specified on the first run of the container)
-d  --destroy   prunes all unused images and containers
"

if [ "$#" -eq 0 ]
then
    echo "$HELP"
    exit 0
fi

VOLUME=$(pwd)/aeneas
BUILD=false
RUN=false
DESTROY=false
IMAGENAME=aeneas

while test $# -gt 0 
do 
    case "$1" in
        -h|--help)
            echo "$HELP"
            exit 0
            ;;
        -b|--build)
            shift
            BUILD=true
            ;;
        -r|--run)
            shift
            RUN=true
            ;;
        -v|--volume)
            shift
            VOLUME="$1"
            shift
            ;;
        -d|--destroy)
            DESTROY=true
            shift
            break
            ;;
        *)
            echo "$HELP"
            exit 0
            ;;
    esac
done

if [ $DESTROY = true ]; then
    docker container stop $IMAGENAME
    docker container prune -f
    docker image prune -f
    exit 0
fi

if [ $BUILD = true ]; then
    docker image build -t $IMAGENAME .
fi

if [ $RUN = true ]; then
    if docker ps -a | grep -q "$IMAGENAME"; then
        docker container start -i $IMAGENAME
    else
        docker container run -it -v "$VOLUME":/workdir --name "$IMAGENAME" "$IMAGENAME"
    fi    
fi