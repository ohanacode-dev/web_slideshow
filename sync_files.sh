#!/bin/bash

SRC=/home/slideshow
DST=192.168.1.100:/home/web_slideshow/slides

rsync -r $SRC/ $DST --delete
