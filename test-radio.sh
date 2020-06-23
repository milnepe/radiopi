#!/bin/sh

# Run test radio player with bbc station list

radiopi/test-radio.py \
    --audio "alsa" \
    --stations "etc/radiopi/stations.bbc.json" \
    --last_station "/home/pi/.radiopi.json"
