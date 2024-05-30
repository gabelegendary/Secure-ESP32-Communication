# client_gui.py

from tkinter import *
from tkinter.ttk import Combobox
from serial.tools.list_ports import comports
import serial_communication
import time

# Global variable to store the serial connection
serial_connection = None

def establish_session():
    global serial_connection, get_temperature_button, toggle_led_button
    
    selected_port = serial_port_combo.get()
    
    if not selected_port:
        log_text.config(state=NORMAL)
        log_text.insert(END, "Please select a serial port.\n", "error")
        log_text.config(state=DISABLED)
        return
    
    serial_connection = serial_communication.initialize_serial(selected_port, 115200)
    
    if serial_connection:
        establish_button.config(text="Close Session", command=close_session)
        log_text.config(state=NORMAL)
        log_text.insert(END, "Connection established.\n", "success")
        log_text.config(state=DISABLED)
        get_temperature_button.config(state=NORMAL)
        toggle_led_button.config(state=NORMAL)
    else:
        log_text.config(state=NORMAL)
        log_text.insert(END, "Failed to establish connection.\n", "error")
        log_text.config(state=DISABLED)

def close_session():
    global serial_connection, get_temperature_button, toggle_led_button
    
    if serial_connection:
        serial_communication.close_serial(serial_connection)
        log_text.config(state=NORMAL)
        log_text.insert(END, "Session closed.\n", "success")
        log_text.config(state=DISABLED)
        establish_button.config(text="Establish Session", command=establish_session)
        serial_connection = None
        get_temperature_button.config(state=DISABLED)
        toggle_led_button.config(state=DISABLED)

def toggle_led():
    global serial_connection
    
    if serial_connection:
        success = serial_communication.send_data(serial_connection, b'T')
        if success:
            if toggle_led_button['text'] == 'Toggle LED':
                toggle_led_button.config(text='Turn LED Off')
                log_text.config(state=NORMAL)
                log_text.insert(END, "LED turned on.\n", "success")
                log_text.config(state=DISABLED)
            else:
                toggle_led_button.config(text='Toggle LED')
                log_text.config(state=NORMAL)
                log_text.insert(END, "LED turned off.\n", "success")
                log_text.config(state=DISABLED)
        else:
            log_text.config(state=NORMAL)
            log_text.insert(END, "Failed to toggle LED.\n", "error")
            log_text.config(state=DISABLED)
    else:
        log_text.config(state=NORMAL)
        log_text.insert(END, "Session not established.\n", "error")
        log_text.config(state=DISABLED)

def get_temperature():
    global serial_connection
    
    if serial_connection:
        serial_communication.send_data(serial_connection, b'temp')
        time.sleep(0.5)  # Small delay to ensure the data is received
        temperature = serial_communication.receive_data(serial_connection)
        if temperature:
            log_text.config(state=NORMAL)
            log_text.insert(END, f"{temperature}\n", "success")
            log_text.config(state=DISABLED)
        else:
            log_text.config(state=NORMAL)
            log_text.insert(END, "Failed to get temperature.\n", "error")
            log_text.config(state=DISABLED)
    else:
        log_text.config(state=NORMAL)
        log_text.insert(END, "Session not established.\n", "error")
        log_text.config(state=DISABLED)

def clear_text(event):
    log_text.config(state=NORMAL)
    log_text.delete(1.0, END)
    log_text.config(state=DISABLED)

def main_gui():
    global establish_button, serial_port_combo, log_text, get_temperature_button, toggle_led_button
    
    display_screen = Tk()
    display_screen.geometry("800x600")
    display_screen.title("Client")

    establish_button = Button(display_screen, text="Establish Session", command=establish_session)
    establish_button.place(x=280, y=10)

    get_temperature_button = Button(display_screen, text="Get Temperature", state=DISABLED, command=get_temperature)
    get_temperature_button.place(x=480, y=10)

    toggle_led_button = Button(display_screen, text="Toggle LED", state=DISABLED, command=toggle_led)
    toggle_led_button.place(x=680, y=10)

    serial_ports = [port.device for port in comports()]
    serial_port_label = Label(display_screen, text="Serial Port:")
    serial_port_label.place(x=10, y=14)
    serial_port_combo = Combobox(display_screen, values=serial_ports, width=15)
    serial_port_combo.place(x=100, y=14)

    log_frame = Frame(display_screen, bg="black")
    log_frame.place(x=20, y=80, width=760, height=500)

    log_text = Text(log_frame, bg="black", fg="white", wrap=WORD, width=80, height=20)
    log_text.pack(expand=YES, fill=BOTH)
    log_text.tag_configure("success", foreground="white")
    log_text.tag_configure("error", foreground="red")

    log_label = Label(display_screen, text="Log:")
    log_label.place(x=20, y=50)

    clear_text_label = Label(display_screen, text="Clear", foreground="blue", cursor="hand2")
    clear_text_label.place(x=730, y=50)
    clear_text_label.bind("<Button-1>", clear_text)

    display_screen.mainloop()

main_gui()
