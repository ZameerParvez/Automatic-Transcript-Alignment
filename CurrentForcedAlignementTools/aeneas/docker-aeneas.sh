#!/bin/bash
HELP=\
"No help"

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
        docker container run -it -v "$VOLUME":/working-folder --name "$IMAGENAME" "$IMAGENAME"
    fi    
fi