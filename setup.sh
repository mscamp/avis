#!/bin/bash

# Install necessary packages
sudo apt install python3 portaudio19-dev espeak-ng mpv pulseaudio jackd -y

# Install tgpt
curl -sSL https://raw.githubusercontent.com/aandrew-me/tgpt/main/install | bash -s /usr/local/bin

# Remove pipewire
sudo apt remove pipewire -y
sudo apt autoremove -y

# Install Python libraries
pip install -r requirements.txt --break-system-packages

# https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi, then reboot