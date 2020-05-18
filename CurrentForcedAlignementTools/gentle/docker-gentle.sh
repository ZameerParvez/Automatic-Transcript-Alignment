#!/bin/bash
HELP=\
"
This is a simple wrapper script to run gentle on port 8080 of the host machine. The docker image is pulled from lowerquality/gentle

To run, use:
    ./docker-gentle.sh -r

-h  --help      print this help message
-r  --run       run the container, if a container named gentle already exists then it will run that
-d  --destroy   prunes all unused images and containers
"

if [ "$#" -eq 0 ]
then
    echo "$HELP"
    exit 0
fi

RUN=false
DESTROY=false
IMAGENAME=gentle

while test $# -gt 0 
do 
    case "$1" in
        -h|--help)
            echo "$HELP"
            exit 0
            ;;
        -r|--run)
            shift
            RUN=true
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

if [ $RUN = true ]; then
    echo "Starting gentle at https://localhost:8080"
    if docker ps -a | grep -q "$IMAGENAME"; then
        docker container start $IMAGENAME
    else
        docker container run -d -p 8080:8765 --name "$IMAGENAME" lowerquality/gentle
    fi    
fi