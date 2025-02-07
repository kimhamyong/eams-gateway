import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Serial Port Configuration
SERIAL_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = int(os.getenv("BAUD_RATE"))

# Sensor Type Mapping
SENSOR_TYPE_MAPPING = {
    0: {"name": "sound", "rf_value": 3},
    1: {"name": "pressure", "rf_value": 4},
    2: {"name": "pir", "rf_value": 5},
}

# Sensor Configuration
allowed_macs = [bytes.fromhex(mac) for mac in os.getenv("SENSOR_MACS", "").split(",")]

# Sensor mac address mapping
sensor_config = {
    mac: SENSOR_TYPE_MAPPING[index % len(SENSOR_TYPE_MAPPING)]
    for index, mac in enumerate(allowed_macs)
}

# Allowed MAC addresses
ALLOWED_MACS = list(sensor_config.keys())