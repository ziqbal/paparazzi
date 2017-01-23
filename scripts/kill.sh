#!/bin/bash

ps aux  |  grep -i "python src/program.py"  |  awk '{print $2}'  |  xargs sudo kill 