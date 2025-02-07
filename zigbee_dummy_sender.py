import serial # brew install socat 사용하여 가상 시리얼 포트 생성
import time

def send_dummy_data(port="/dev/ttys010", baudrate=9600):
    """
    Send dummy ZigBee API 2 frame data to simulate sensor transmission.
    """
    dummy_frame = bytes.fromhex("7E 00 0D 90 00 7D 33 A2 00 41 FC B7 A4 12 9A 01 34 34")

    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Sending dummy data to {port}...")
            while True:
                ser.write(dummy_frame)  # Send the fake ZigBee frame
                print(f"Sent: {dummy_frame.hex().upper()}")
                time.sleep(3)  # Send data every 3 seconds
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    send_dummy_data()
