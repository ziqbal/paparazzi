#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
APP=${PWD##*/}     

############################################################

#git fetch --all
#git reset --hard origin/master

echo "......................................................"

git add .
git commit -m "gitup" .
git push

echo "......................................................"

git status

echo "......................................................"

