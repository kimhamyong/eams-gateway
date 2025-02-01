import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv #개발 환경 맥으로 임시 변경

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

# 발행할 JSON 메시지 예시
MESSAGE = {
    "gateway_id": "home1",
    "sensor": "sen1",
    "value": 1,
    "timestamp": "2025-01-23T12:00:00Z"
}

def main():
    """MQTT 메시지를 JSON 형식으로 발행"""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    try:
        print(f"🚀 Connecting to MQTT Broker at {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, 60)

        json_message = json.dumps(MESSAGE)  # JSON 직렬화
        print(f"📤 Publishing JSON message to '{TOPIC}': {json_message}")
        client.publish(TOPIC, json_message, qos=0)

        client.disconnect()
        print("✅ Message published and MQTT client disconnected.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
