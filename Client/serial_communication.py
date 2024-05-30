# serial_communication.py

import serial

def initialize_serial(port_name, baud_rate):
    try:
        serial_connection = serial.Serial(port_name, baud_rate, timeout=1)
        if serial_connection.is_open:
            print(f"Port {port_name} opened successfully.")
            return serial_connection
        else:
            print("Failed to open port.")
            return None
    except serial.SerialException as e:
        print(f"Error opening port {port_name}: {e}")
        return None

def send_data(serial_connection, data):
    try:
        serial_connection.write(data + b'\n')
        return True
    except serial.SerialException as e:
        print(f"Error sending data: {e}")
        return False

def receive_data(serial_connection):
    try:
        data = b""
        while serial_connection.in_waiting > 0:
            data += serial_connection.readline()
        decoded_data = data.decode().strip()
        print(f"Received data: {decoded_data}")  # Debug: Print received data
        return decoded_data
    except serial.SerialException as e:
        print(f"Error receiving data: {e}")
        return None

def close_serial(serial_connection):
    try:
        serial_connection.close()
    except serial.SerialException as e:
        print(f"Error closing port: {e}")
