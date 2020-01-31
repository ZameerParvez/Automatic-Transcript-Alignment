#!/bin/bash
HELP=\
"No help"

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
    exit 0
fi

echo "Starting gentle at https://localhost:8080"
if [ $RUN = true ]; then
    if docker ps -a | grep -q "$IMAGENAME"; then
        docker container start $IMAGENAME
    else
        docker container run -d -p 8080:8765 --name "$IMAGENAME" lowerquality/gentle
    fi    
fi