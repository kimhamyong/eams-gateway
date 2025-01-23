import serial
import time
def main():
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
        print("Connected to /dev/ttyUSB0")
        while True:
            try:
                raw_data = ser.read(1024)
                if raw_data:
                    print(f"Received Raw Data: {raw_data.hex()}")
                else:
                    print("No data received.")
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