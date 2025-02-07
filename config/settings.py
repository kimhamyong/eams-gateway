import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

# Serial Port Configuration
SERIAL_PORT = os.getenv("SERIAL_PORT")

# Sensor Type Mapping
SENSOR_TYPE_MAPPING = {
    "sound": 3,
    "pressure": 4,
    "pir": 5,
}

# Sensor Configuration
allowed_macs = [bytes.fromhex(mac) for mac in os.getenv("SENSOR_MACS", "").split(",")]

# Sensor mac address mapping
sensor_config = {
    mac: {"name": sensor_type, "rf_value": rf_value}
    for mac, (sensor_type, rf_value) in zip(allowed_macs, SENSOR_TYPE_MAPPING.items())
}

# Allowed MAC addresses
ALLOWED_MACS = list(sensor_config.keys())