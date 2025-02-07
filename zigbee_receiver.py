import serial
import time
from datetime import datetime
from mqtt_publisher import publish_message  # MQTT 발행 함수 가져오기
from config.settings import ALLOWED_MACS, SERIAL_PORT, sensor_config, gateway_id

def decode_escaped_mac(frame):
    """
    Decode the escaped MAC address from an API 2 Mode frame.
    """
    source_mac = []
    escape_next = False
    
    for byte in frame:
        if escape_next:
            source_mac.append(byte ^ 0x20)
            escape_next = False
        elif byte == 0x7D:
            escape_next = True
        else:
            source_mac.append(byte)
    
    return bytes(source_mac)


def verify_checksum(frame):
    """
    Verify the checksum of a received ZigBee API 2 frame.
    Returns True if the checksum is valid, False otherwise.
    """
    if len(frame) < 5:
        return False

    frame_data = frame[3:-1]  # Frame Type(1 byte) + Frame Data
    decoded_data = decode_escaped_mac(frame_data)

    calculated_checksum = (0xFF - (sum(decoded_data) & 0xFF)) & 0xFF
    actual_checksum = frame[-1]

    return calculated_checksum == actual_checksum


def process_frame(frame):
    """
    Process the received frame and return MQTT payload if valid.
    """
    if frame[0] != 0x7E: 
        return None

    frame_length = (frame[1] << 8) | frame[2]
    if len(frame[4:]) != frame_length + 1:
        return None

    frame_type = frame[3]
    if frame_type != 0x90:
        return None

    source_mac = decode_escaped_mac(frame[4:13])
    if source_mac not in ALLOWED_MACS:
        return None

    if not verify_checksum(frame):
        return None

    rf_value = int(chr(frame[16]))  # RF 값을 정수로 변환

    sensor_info = sensor_config[source_mac]

    # RF 값 일치 여부 확인
    if sensor_info["rf_value"] != rf_value:
        print(f"RF Value Mismatch: Expected {sensor_info['rf_value']}, Got {rf_value}")
        return None

    return {
        "gateway_id": gateway_id,
        "sensor": sensor_info["name"],
        "value": 1,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def main():
    try:
        ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        buffer = bytearray()

        while True:
            try:
                raw_data = ser.read(1024)

                if raw_data:
                    buffer.extend(raw_data)

                    while len(buffer) >= 4:
                        if buffer[0] != 0x7E:
                            buffer.pop(0)
                            continue

                        if len(buffer) < 3:
                            break
                        frame_length = (buffer[1] << 8) | buffer[2]
                        total_length = frame_length + 5

                        if len(buffer) < total_length:
                            break

                        frame = buffer[:total_length]
                        buffer = buffer[total_length:]

                        payload = process_frame(frame)
                        if payload:
                            print(f"Publishing MQTT message: {payload}")
                            publish_message(payload)  # MQTT 발행
                else:
                    time.sleep(1)
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")


if __name__ == "__main__":
    main()
