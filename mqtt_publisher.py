import os
import paho.mqtt.client as mqtt

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = "/test" 
MESSAGE = "hi" 

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    
    try:
        print(f"Connecting to broker {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, 60)
        
        print(f"Publishing message '{MESSAGE}' to topic '{TOPIC}'")
        client.publish(TOPIC, MESSAGE)
        
        client.disconnect()
        print("Message published and disconnected.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
