import time
import serial_communication
from mbedtls import pk, hmac, hashlib, cipher

RSA_SIZE = 2048
EXPONENT = 65537

SECRET_KEY = b"Fj2-;wu3Ur=ARl2!Tqi6IuKM3nG]8z1+"

# Initialize HMAC key
hmac_key = hashlib.sha256()
hmac_key.update(SECRET_KEY)
hmac_key = hmac_key.digest()
hmac_instance = hmac.new(hmac_key, digestmod="SHA256")

def send_datas(serial_connection, buf: bytes):
    hmac_instance.update(buf)
    hmac_digest = hmac_instance.digest()
    buf += hmac_digest
    serial_communication.send_data(serial_connection, buf)
    print("Key hashed:", buf.hex())
    print("Sent")

def session_init(serial_connection):
    # Generate RSA key pair
    rsa_temp = pk.RSA()
    rsa_temp.generate(RSA_SIZE, EXPONENT)
    
    # Export the public key
    temp_public_key = rsa_temp.export_public_key()
    print("Generated RSA Public Key:", temp_public_key.hex())
    
    # Send the public key with HMAC
    send_datas(serial_connection, temp_public_key)

if __name__ == "__main__":
    serial_port = '/dev/cu.usbserial-1130'
    serial_baudrate = 115200
    serial_connection = serial_communication.initialize_serial(serial_port, serial_baudrate)
    if serial_connection:
        session_init(serial_connection)
    else:
        print("Failed to establish serial connection.")
