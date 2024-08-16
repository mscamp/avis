#!/bin/bash

# Variables
HOURS=$1 
MINUTES=$2
SECONDS=$3
SOUND=$4

# Wait for specified time
sleep "${HOURS}h" "${MINUTES}m" "${SECONDS}s"

# Kills mpv
pkill mpv

# Play a tune
mpv "${SOUND}"