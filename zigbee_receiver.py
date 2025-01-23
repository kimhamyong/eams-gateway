import serial
import time

def process_frame(frame):
    """
    Process the received frame and print its contents.
    """
    print(f"Received Data: {frame.hex()}")

def main():
    try:
        ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
        print("Connected to /dev/ttyUSB0")

        buffer = bytearray()  # Buffer to store incoming data

        while True:
            try:
                raw_data = ser.read(1024)  # Read up to 1024 bytes
                if raw_data:
                    buffer.extend(raw_data)  # Add received data to the buffer

                    # Extract and process frames from the buffer
                    while len(buffer) >= 4:  # Check for minimum frame length
                        if buffer[0] != 0x7E:  # Check for frame start delimiter
                            buffer.pop(0)  # Remove invalid data
                            continue

                        # Extract frame length
                        if len(buffer) < 3:
                            break
                        frame_length = (buffer[1] << 8) | buffer[2]
                        total_length = frame_length + 4  # Header (3) + Checksum (1)

                        if len(buffer) < total_length:
                            break  # Wait for the complete frame to arrive

                        # Extract the complete frame
                        frame = buffer[:total_length]
                        buffer = buffer[total_length:]  # Remove processed data from buffer

                        # Process the frame
                        process_frame(frame)
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
