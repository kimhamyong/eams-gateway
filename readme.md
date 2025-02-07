## Overview
The Home Gateway connects ZigBee-based sensors to an MQTT broker for real-time IoT data exchange. It receives sensor data through a ZigBee USB module, processes it, and sends structured messages to a central server via the MQTT broker.

## Environment
```
- OS: Ubuntu 24.10 (GNU/Linux 6.11.0-1004-raspi aarch64)  
- Hardware: Raspberry Pi 3B+  
- Python: 3.12.7  
- Python MQTT Library: python3-paho-mqtt 2.0.0-1
- MQTT Broker: Mosquitto 2.0.18  
```

## Architecture & Components
```
 ┌──────────────┐     ┌─────────────────────┐     ┌────────────────────┐     ┌─────────────────┐     ┌────────────┐
 │   End Node   │  →  │   ZigBee Receiver   │  →  │   MQTT Publisher   │  →  │   MQTT Broker   │  →  │   Server   │ 
 └──────────────┘     └─────────────────────┘     └────────────────────┘     └─────────────────┘     └────────────┘
```

### ZigBee Receiver (Serial Communication) 
 - _**ZigBee router `MAC addresses` must be listed in the `.env` file, separated by commas**_
 - Configure the ZigBee module as a **Coordinator** using XCTU and connect it to the hardware via a USB adapter  
 - Receives data in API 2 Mode (escaped mode)
 - Sound, Pressure, and PIR sensors are mapped to specific MAC addresses, **rf_value**, and sensor names
 - Only allowed MAC addresses are processed; data from unlisted MAC addresses is ignored  

### MQTT Publisher (Paho MQTT) 
 - _**Configure the **MQTT topic (`gateway_id`)** in the `.env` file**_
 - Publishes processed sensor data to an MQTT broker
 - Uses 'paho-mqtt' for MQTT communication  
 - The MQTT topic is dynamically set based on 'gateway_id'
 - Converts sensor data into **JSON format** before publishing: 
    ```json
    {  
        "gateway_id": "home1",                      # Identifies the gateway
        "sensor": "pir",                            # Sensor type (sound, pressure, pir, etc.)
        "value": 1,                                 # triggered event
        "timestamp": "2025-01-23T12:00:00Z"         # ISO 8601 format
    }
    ```

### MQTT Broker (Mosquitto)
 - _**Specify the **MQTT broker `IP addres`s and `port`** in the `.env` file**_
 - Manages MQTT message exchange between clients
 - Requires **authentication** (allow_anonymous false)
 - Listens on a configurable **port** (default: 1883)


## File Structure
```
home-gateway/  
│── config/  
│   ├── settings.py           # Loads environment variables and system settings
│── mqtt/  
│   ├── publisher.py          # Publishes sensor data to the MQTT broker 
│── zigbee/  
│   ├── parser.py             # Parses and validates ZigBee frames  
│   ├── receiver.py           # Reads ZigBee data from the serial Port  
│── main.py  
│── mqtt-broker.sh            # Script to install and configure the Mosquitto MQTT broker  
└── setup.sh                  # Setup script for dependencies and environment configuration  
```

## Setup & Installation
### 1. Install Dependencies
Run the setup script to install all necessary dependencies:
```bash
chmod +x setup.sh
./setup.sh
```
This will install python3-paho-mqtt, detect the ZigBee USB module at /dev/ttyUSB*, and ensure the user belongs to the dialout group for serial access.

### 2. Configure the Environment
Modify the `.env` file to set the appropriate values for ZigBee and MQTT.

### 3. Install & Configure the MQTT Broker
Run the MQTT broker setup script:
```bash
chmod +x mqtt-broker.sh
./mqtt-broker.sh
```
This will install python3-paho-mqtt, detect the ZigBee USB module at /dev/ttyUSB*, and ensure the user belongs to the dialout group for serial access.