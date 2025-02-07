import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER") 
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")


def publish_message(payload):
    """
    Publish a message to the MQTT Broker
    """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) # create a new MQTT client

    try:
        print(f"🚀 Connecting to MQTT Broker at {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, 60) # connect to the MQTT broker

        json_message = json.dumps(payload) # convert payload to JSON
        print(f"📤 Publishing message to '{TOPIC}': {json_message}")
        client.publish(TOPIC, json_message, qos=0) # publish message to the topic

        client.disconnect() # disconnect from the MQTT broker
        print("✅ Message published and MQTT client disconnected.")

    except Exception as e: # handle exceptions
        print(f"❌ Error: {e}")
        client.disconnect() # disconnect from the MQTT broker