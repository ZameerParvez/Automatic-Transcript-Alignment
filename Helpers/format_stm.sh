#!/bin/bash

HELP=\
"
This script can trim the timestamp and file identifiers from all lines in the input file, e.g.AA 1 AA 726.72 729.4 <NA>

Useage:

    ./trim-stm.sh <in-file> <out-file>

"

if [ "$#" -eq 0 ]
then
    echo "$HELP"
    exit 0
fi

INFILE=$1
OUTFILE=$2

< "$INFILE" sed -r "s/^[^>]*> /\n/" > "$OUTFILE"