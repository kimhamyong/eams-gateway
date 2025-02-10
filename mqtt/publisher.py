import os
import json
import paho.mqtt.client as mqtt
from config.settings import gateway_id, MQTT_BROKER, MQTT_PORT

# MQTT Topic for publishing messages
TOPIC = f"{gateway_id[:-1]}/{gateway_id[-1]}" 

def publish_message(payload):
    """
    Publish a message to the MQTT Broker
    """
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1) # create a new MQTT client

    try:
        print(f"🚀 Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60) # connect to the MQTT broker

        json_message = json.dumps(payload) # convert payload to JSON
        print(f"📤 Publishing message to '{TOPIC}': {json_message}")
        client.publish(TOPIC, json_message, qos=0) # publish message to the topic

        client.disconnect() # disconnect from the MQTT broker
        print("✅ Message published and MQTT client disconnected.")

    except Exception as e: # handle exceptions
        print(f"❌ Error: {e}")
        client.disconnect() # disconnect from the MQTT broker