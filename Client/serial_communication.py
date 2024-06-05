import serial
import serial.tools.list_ports

ser: serial.Serial  # Serial connection object

def initialize_serial(port, baudrate) -> bool:
    global ser
    ser = serial.Serial(port, baudrate)
    return ser.is_open

def send_data(data) -> bool:
    global ser
    ret = False
    if ser.is_open == True:
        ret = (len(data) == ser.write(data))  # Send
    return ret
    

def receive_data(size: int):
    global ser
    data = bytes()
    if ser.is_open == True:
        data = ser.read(size)
    return data


def close_serial():
    global ser
    try:
        if ser.is_open:
            ser.close()
    except serial.SerialException:
        pass
