#!/bin/bash

echo "Installing and configuring Mosquitto MQTT broker..."

# Install Mosquitto
echo "Installing Mosquitto..."
sudo apt update && sudo apt-get install -y mosquitto

# Check Mosquitto status
echo "Checking Mosquitto status..."
sudo /etc/init.d/mosquitto status

# Prompt user for MQTT username, user has to enter the username
read -p "Enter MQTT username: " MQTT_USER # e.g. username

# Add MQTT user
echo "Creating MQTT user '$MQTT_USER'..."
sudo mosquitto_passwd -c /etc/mosquitto/passwd $MQTT_USER

# Change ownership of Mosquitto password file
sudo chown mosquitto:mosquitto /etc/mosquitto/passwd

# Prompt user for MQTT listener port, user has to enter the port number
read -p "Enter MQTT listener port (default: 1883): " MQTT_PORT # e.g. 1883
MQTT_PORT=${MQTT_PORT:-1883}  # Set default port to 1883 if empty

# Configure Mosquitto settings
echo "Configuring Mosquitto..."
sudo bash -c "cat > /etc/mosquitto/mosquitto.conf <<EOF
allow_anonymous false
password_file /etc/mosquitto/passwd
listener $MQTT_PORT
EOF"

# Restart Mosquitto and enable auto-start on boot
echo "Restarting and enabling Mosquitto service..."
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto  # Ensure Mosquitto starts on boot
sudo systemctl status mosquitto

# Check if Mosquitto is listening on port and disable firewall if necessary
echo "Checking if Mosquitto is listening on port $MQTT_PORT..."
if ! sudo ss -tlnp | grep -q ":$MQTT_PORT "; then
    echo "Port $MQTT_PORT is not open. Disabling firewall..."
    sudo ufw allow $MQTT_PORT/tcp
    echo "Restarting Mosquitto..."
    sudo systemctl restart mosquitto
fi

echo "Mosquitto setup complete!"