#!/bin/bash

curdir=$(dirname "$0")
gunicorn -b 0.0.0.0:8000 -w 3 display:app





