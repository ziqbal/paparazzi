#!/bin/bash

CWD="$(pwd)"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

#export DISPLAY=:0.0

#flock -xn f.lock -c "python src/program.py" &
flock -xn f.lock -c "python src/program.py" &

pwd

cd $CWD