import serial
import time
from zigbee.parser import process_frame
from mqtt.publisher import publish_message
from config.settings import SERIAL_PORT

def start_receiver():
    """
    Start the ZigBee receiver, process incoming frames, and publish valid data to MQTT.
    """
    try:
        ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1) # connect to serial port
        print(f"Connected to {SERIAL_PORT}") # print connected message

        buffer = bytearray() # create a byte array

        while True:
            try:
                raw_data = ser.read(1024) # read data from serial port

                if raw_data:
                    buffer.extend(raw_data) # add data to buffer

                    while len(buffer) >= 4: # check if buffer has enough data
                        if buffer[0] != 0x7E: # check if the first byte is 0x7E
                            buffer.pop(0) # remove the first byte and
                            continue

                        if len(buffer) < 3: # check if buffer has enough data
                            break
                        frame_length = (buffer[1] << 8) | buffer[2] # calculate frame length
                        total_length = frame_length + 5 # calculate total length

                        if len(buffer) < total_length: # check if buffer has enough data
                            break

                        frame = buffer[:total_length] # extract frame from buffer
                        buffer = buffer[total_length:] # remove frame from buffer

                        payload = process_frame(frame) # process frame
                        if payload:
                            print(f"Publishing MQTT message: {payload}") 
                            publish_message(payload) # publish message to MQTT
                else:
                    time.sleep(1) # sleep for 1 second
            except serial.SerialException as e: # handle serial exception
                print(f"Serial error: {e}")
                break
    except Exception as e: # handle other exceptions
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open: # check if serial port is open
            ser.close() # close serial port
            print("Serial port closed.")
