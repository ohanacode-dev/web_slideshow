#!/bin/bash

curdir=$(dirname "$0")

sleep 600

cd /tmp
git clone git@github.com:ohanacode-dev/web_slideshow.git
rsync -r web_slideshow ~







