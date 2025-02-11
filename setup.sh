#!/bin/bash

echo "Setting up Python environment and checking serial ports..."

# Install paho-mqtt
echo "Installing python3-paho-mqtt and python3-dotenv..."
sudo apt update && sudo apt install -y python3-paho-mqtt python3-dotenv

# Check connected USB serial devices
echo "Checking connected USB serial devices..."
ls -l /dev/ttyUSB*

# Check user groups
echo "Checking user groups..."
groups

echo "*** Setup complete! If 'dialout' is not in the group list, add your user to it: ***"
echo "sudo usermod -aG dialout \$USER && exec newgrp dialout"
