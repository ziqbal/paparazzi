#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

ssh pi@192.168.1.15 'tar zcvf tmp.tar.gz /tmp/*.jpg'
scp pi@192.168.1.15:tmp.tar.gz /tmp/tmp.tar.gz
ssh pi@192.168.1.15 'rm tmp.tar.gz'
cd /tmp/
tar zxvf tmp.tar.gz
open tmp

