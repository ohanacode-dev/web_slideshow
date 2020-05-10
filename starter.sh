#!/bin/bash

curdir=$(dirname "$0")
cd /tmp
git clone git@github.com:ohanacode-dev/web_slideshow.git
rsync -r web_slideshow ~

gunicorn -b 0.0.0.0:8000 -w 3 display:app





