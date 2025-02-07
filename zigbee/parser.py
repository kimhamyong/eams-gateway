from datetime import datetime
from config.settings import ALLOWED_MACS, sensor_config, gateway_id

def decode_escaped_mac(frame):
    """
    Decode the escaped MAC address from an API 2 Mode frame.
    """
    source_mac = []
    escape_next = False
    
    for byte in frame: # iterate over each byte in the frame
        if escape_next:
            source_mac.append(byte ^ 0x20) # append the byte XORed with 0x20
            escape_next = False # reset escape_next
        elif byte == 0x7D: # check if byte is 0x7D
            escape_next = True # set escape_next to True
        else:
            source_mac.append(byte) # append the byte
    
    return bytes(source_mac) # return the MAC address as bytes


def verify_checksum(frame):
    """
    Verify the checksum of a received ZigBee API 2 frame.
    Returns True if the checksum is valid, False otherwise.
    """
    if len(frame) < 5: # check if frame length is less than 5
        return False

    frame_data = frame[3:-1] # Frame Type(1 byte) + Frame Data
    decoded_data = decode_escaped_mac(frame_data) # decode the frame data

    calculated_checksum = (0xFF - (sum(decoded_data) & 0xFF)) & 0xFF # calculate the checksum
    actual_checksum = frame[-1] # get the actual checksum

    return calculated_checksum == actual_checksum # return True if checksums match, False otherwise


def process_frame(frame):
    """
    Parse and validate a received ZigBee frame. Returns MQTT payload if valid.
    """
    if frame[0] != 0x7E: # check if the first byte is 0x7E
        return None

    frame_length = (frame[1] << 8) | frame[2] # calculate frame length
    if len(frame[4:]) != frame_length + 1: # check if frame length is correct
        return None

    frame_type = frame[3] # get the frame type
    if frame_type != 0x90: # check if frame type is 0x90
        return None

    source_mac = decode_escaped_mac(frame[4:13]) # decode the MAC address
    if source_mac not in ALLOWED_MACS: # check if MAC address is allowed
        print(f"Ignored Frame from MAC Address: {source_mac.hex().upper()}") 
        return None

    if not verify_checksum(frame): # check if checksum is valid
        return None

    rf_value = int(chr(frame[16])) # convert RF value to integer

    sensor_info = sensor_config.get(source_mac) # get sensor info from config
    if not sensor_info: # check if sensor info is available
        print(f"Unknown MAC Address: {source_mac.hex().upper()}") 
        return None

    if sensor_info["rf_value"] != rf_value: # check if RF value matches
        print(f"RF Value Mismatch: Expected {sensor_info['rf_value']}, Got {rf_value}")
        return None

    # return MQTT payload
    return { 
        "gateway_id": gateway_id,
        "sensor": sensor_info["name"],
        "value": 1,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
