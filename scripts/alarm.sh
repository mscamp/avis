#!/bin/bash

# Variables
HOURS=$1 
MINUTES=$2
SECONDS=$3
SOUND=$4
NAME=$5
WAIT=$6
LIGHTS_SCRIPT=$7

# Wait for specified time
sleep "${HOURS}h" "${MINUTES}m" "${SECONDS}s"

# Play a tune
mpv "${SOUND}" &

# Turn on lights
python "${LIGHTS_SCRIPT}"

# Stop alarm after specified time
sleep $WAIT
pkill mpv

# Good morning
espeak-ng -v roa/it "Buongiorno ${NAME}"