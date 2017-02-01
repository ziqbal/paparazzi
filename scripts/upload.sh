#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     


IP="192.168.1.15"

############################################################

rm -rf f.lock

cd ..

rm -rf /tmp/$APP.tar.gz


find $APP -type f | egrep -v '\.git|\.log' | xargs tar zcvf /tmp/$APP.tar.gz

cd $APP

############################################################

scp /tmp/$APP.tar.gz pi@$IP:$APP.tar.gz 

ssh pi@$IP "sudo ./$APP/scripts/kill.sh"
ssh pi@$IP "tar zxvf $APP.tar.gz"
ssh pi@$IP "rm $APP.tar.gz"
