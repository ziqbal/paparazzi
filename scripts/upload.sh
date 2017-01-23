#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

scp /tmp/$APP.tar.gz pi@192.168.1.13:$APP.tar.gz 