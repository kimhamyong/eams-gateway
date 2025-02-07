import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")


def publish_message(payload):
    """MQTT 메시지를 JSON 형식으로 발행"""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    try:
        print(f"🚀 Connecting to MQTT Broker at {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, 60)

        json_message = json.dumps(payload)  # JSON 직렬화
        print(f"📤 Publishing JSON message to '{TOPIC}': {json_message}")
        client.publish(TOPIC, json_message, qos=0)

        client.disconnect()
        print("✅ Message published and MQTT client disconnected.")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("This script is for publishing MQTT messages. Import and use `publish_message()`.")
