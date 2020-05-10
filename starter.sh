#!/bin/bash

#sleep 10
gunicorn -b 0.0.0.0:8000 -w 3 display:app





