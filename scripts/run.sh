#!/bin/bash

CWD="$(pwd)"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

flock -xn f.lock -c "python src/program.py" &

cd $CWD