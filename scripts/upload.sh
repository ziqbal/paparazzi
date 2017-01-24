#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

scp /tmp/$APP.tar.gz pi@cassopi:$APP.tar.gz 