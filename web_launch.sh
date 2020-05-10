#!/bin/bash

cd $(dirname "$0")
./starter.sh &
./updater.sh &

firefox -url http://localhost:8000 &
xdotool mousemove_relative 2000 0
sleep 5
xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11



