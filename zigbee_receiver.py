import serial
import time

ALLOWED_MACS = [
    bytes.fromhex("0013A20041FCBBBC"),
    bytes.fromhex("0013A20041FCB7A4"),
    bytes.fromhex("0013A200418F27CB")
]


def decode_escaped_mac(frame):
    """
    Decode the escaped MAC address from an API 2 Mode frame.
    """
    source_mac = []
    escape_next = False
    
    for byte in frame:  # Iterate over each byte in the MAC address
        if escape_next:
            source_mac.append(byte ^ 0x20)  # XOR with 0x20 to get the original byte
            escape_next = False # Reset escape flag
        elif byte == 0x7D:
            escape_next = True  # Next byte will be escaped
        else:
            source_mac.append(byte) # Add the byte as is
    
    return bytes(source_mac) # Convert the list to bytes


def verify_checksum(frame):
    """
    Verify the checksum of a received ZigBee API 2 frame.
    Returns True if the checksum is valid, False otherwise.
    """
    if len(frame) < 5:
        print("Invalid frame: Too short to contain a checksum.")
        return False

    # Extract frame data (excluding start delimiter and length)
    frame_data = frame[3:-1]  # Frame Type(1 byte) + Frame Data

    # Unescape the frame data
    decoded_data = decode_escaped_mac(frame_data)

    # Calculate the checksum
    calculated_checksum = (0xFF - (sum(decoded_data) & 0xFF)) & 0xFF

    # Extract the actual checksum from the frame
    actual_checksum = frame[-1]

    # Compare the calculated and actual checksums
    if calculated_checksum == actual_checksum:
        return True
    else:  # Print an error message if the checksums don't match
        print(f"Expected {calculated_checksum:02X}, Got {actual_checksum:02X}")
        return False


def process_frame(frame):
    """
    Process the received frame, filter by allowed MAC addresses, and print its contents.
    """
    # Check for the start delimiter
    if frame[0] != 0x7E: 
        print("Invalid Frame: Missing Start Delimiter")
        return  # Ignore frames without the start delimiter

    # Extract frame length
    frame_length = (frame[1] << 8) | frame[2]
    if len(frame[4:]) != frame_length + 1:
        print(f"Invalid Frame: Length Mismatch (Expected {frame_length}, Got {len(frame[4:]) - 1})")
        return  # Ignore frames with incorrect length

    # Check frame type (0x90 = RX Indicator)
    frame_type = frame[3]
    if frame_type != 0x90:
        print(f"Unsupported Frame Type: {frame_type:02X}")
        return  # Ignore non-RX frames

    # Decode source MAC address
    source_mac = decode_escaped_mac(frame[4:13])   # Decode escape sequence
    if source_mac not in ALLOWED_MACS:
        print(f"Ignored Frame from MAC Address: {source_mac.hex().upper()}")
        return  # Ignore frames from unallowed MAC addresses
    
    # Verify checksum
    if not verify_checksum(frame):
        print("Checksum Error: ")
        return # Ignore frames with invalid checksum

    # Print allowed frame data
    print(f"Received Data: {chr(frame[16])}")


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
