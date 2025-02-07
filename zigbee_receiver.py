import serial
import time

ALLOWED_MACS = [
    b'\x00\x7D\x33\xA2\x00\x41\xFC\xB7\xA4',  
    b'\x00\x7D\x33\xA2\x00\x41\xFC\xBB\xBC', 
    b'\x00\x7D\x33\xA2\x00\x41\x8F\x27\xCB' 
]

def process_frame(frame):
    """
    Process the received frame, filter by allowed MAC addresses, and print its contents.
    """
    if frame[0] != 0x7E:  # Start delimiter
        print("Invalid Frame: Missing Start Delimiter")
        return

    # Extract frame length
    frame_length = (frame[1] << 8) | frame[2]
    if len(frame[4:]) != frame_length + 1:
        print(f"Invalid Frame: Length Mismatch (Expected {frame_length}, Got {len(frame[4:]) - 1})")
        return

    # Check frame type (0x90 = RX Indicator)
    frame_type = frame[3]
    if frame_type != 0x90:
        print(f"Unsupported Frame Type: {frame_type:02X}")
        return

    # Decode source MAC address
    source_mac = frame[4:13]  # Decode escape sequence
    if source_mac not in ALLOWED_MACS:
        print(f"Ignored Frame from MAC Address: {source_mac.hex().upper()}")
        return  # Ignore frames from unallowed MAC addresses

    # Print allowed frame data
    print(f"Received Data: {frame[16]:02X}")

def main():
    try:
        ser = serial.Serial('/dev/ttys011', baudrate=9600, timeout=1) #ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)
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
                        total_length = frame_length + 5  # Start Delimiter(1) + Length(2) + Frame Type(1) + Checksum (1)

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
