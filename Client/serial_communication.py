import serial

def initialize_serial(port_name, baud_rate):
    try:
        serial_connection = serial.Serial(port_name, baud_rate, timeout=1)
        if serial_connection.is_open:
            return serial_connection
        else:
            return None
    except serial.SerialException:
        return None

def send_data(serial_connection, data):
    try:
        serial_connection.write(data)
        return True
    except serial.SerialException:
        return False

def receive_data(serial_connection, expected_length):
    try:
        data = serial_connection.read(expected_length)
        if len(data) == expected_length:
            return data
        else:
            return None
    except serial.SerialException:
        return None

def close_serial(serial_connection):
    try:
        if serial_connection.is_open:
            serial_connection.close()
    except serial.SerialException:
        pass
