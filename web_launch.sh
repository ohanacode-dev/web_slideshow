#!/bin/bash

cd $(dirname "$0")
./starter.sh &

firefox -url http://localhost:8000 &

sleep 5

xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11



