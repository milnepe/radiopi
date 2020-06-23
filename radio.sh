#!/bin/sh

# Run radio player with global station lists

radiopi/radio.py \
    --audio "alsa" \
    --stations "etc/radiopi/stations.json" \
    --last_station "/home/pi/.radiopi.json"
