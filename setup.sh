#!/bin/bash

# Install necessary packages
sudo apt install portaudio19-dev espeak-ng mpv pulseaudio jackd -y

# Remove pipewire
sudo apt remove pipewire -y
sudo apt autoremove -y

# Install Python libraries
pip install -r requirements.txt --break-system-packages

# https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi, then reboot