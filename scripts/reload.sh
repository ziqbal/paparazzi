#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

cd ..

./paparazzi/scripts/kill.sh 
sleep 2 
tar zxvf paparazzi.tar.gz
sudo ./paparazzi/scripts/run.sh

