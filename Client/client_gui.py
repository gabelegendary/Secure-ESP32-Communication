from tkinter import *
from tkinter.ttk import Combobox
from serial.tools.list_ports import comports
from client_exchange import Session

class SecureClientApp:
    def __init__(self, master, select_options):
        self.master = master
        self.serial_connection = None
        self.session = None
        self.setup_ui(select_options)

    def setup_ui(self, select_options):
        self.master.title("Secure Client")
        self.master.geometry("800x600")

        self.establish_button = Button(self.master, text="Establish Session", command=self.establish_session, state=DISABLED)
        self.establish_button.place(x=300, y=10)

        self.get_temperature_button = Button(self.master, text="Get Temperature", command=self.get_temperature, state=DISABLED)
        self.get_temperature_button.place(x=480, y=10)

        self.toggle_led_button = Button(self.master, text="TURN LED ON", command=self.toggle_led, state=DISABLED)
        self.toggle_led_button.place(x=660, y=10)

        serial_port_label = Label(self.master, text="Select Serial Port:")
        serial_port_label.place(x=10, y=14)
        self.serial_port_combo = Combobox(self.master, values=select_options, width=15)
        self.serial_port_combo.place(x=130, y=14)
        self.serial_port_combo.bind("<<ComboboxSelected>>", self.update_button_state)

        log_frame = Frame(self.master, bg="black")
        log_frame.place(x=20, y=80, width=760, height=500)

        self.log_text = Text(log_frame, bg="black", fg="white", wrap=WORD, width=80, height=20)
        self.log_text.pack(expand=YES, fill=BOTH)

        log_label = Label(self.master, text="Log:")
        log_label.place(x=20, y=50)

        clear_log_label = Label(self.master, text="Clear Log", foreground="blue", cursor="hand2")
        clear_log_label.place(x=710, y=50)
        clear_log_label.bind("<Button-1>", self.clear_log)

    def establish_session(self):
        success = Session.select()
        if not success:
            self.print_log("Please select a serial port.")
            self.establish_button.config(state=DISABLED)
            return

        if success:
            self.print_log("Session established successfully")
            self.establish_button.config(text="Close Session", command=self.close_session)
            self.get_temperature_button.config(state=NORMAL)
            self.toggle_led_button.config(state=NORMAL)
            self.session = Session(self.serial_port_combo.get())
        else:
            self.print_log("Failed to establish session")
            self.get_temperature_button.config(state=DISABLED)
            self.toggle_led_button.config(state=DISABLED)

    def close_session(self):
        if self.session:
            self.session.close_serial()
            self.session = None
            self.print_log("Session closed successfully.")
            self.establish_button.config(text="Establish Session", command=self.establish_session)
            self.get_temperature_button.config(state=DISABLED)
            self.toggle_led_button.config(state=DISABLED)
        else:
            self.print_log("No active session to close.")

    def get_temperature(self):
        received_bytes = self.session.get_temperature()
        if received_bytes is not None:
            try:
                temperature = received_bytes.decode("utf-8")
                message = f"Temperature: {temperature} °C"
                self.print_log(message)
            except Exception as e:
                self.print_log(f"Error decoding temperature: {str(e)}")
        else:
            self.print_log("Failed to retrieve temperature")

    def toggle_led(self):
        state = self.session.toggle_led()
        if state is not None:
            try:
                state_str = state.decode("utf-8").strip('\x00')
                if state_str == "1":
                    self.print_log("LED Turned ON")
                    self.toggle_led_button.config(text="TURN LED OFF")
                elif state_str == "0":
                    self.print_log("LED Turned OFF")
                    self.toggle_led_button.config(text="TURN LED ON")
                else:
                    self.print_log("Unexpected LED status response")
            except Exception as e:
                self.print_log(f"Error decoding LED status: {str(e)}")
        else:
            self.print_log("Failed to toggle LED")

    def clear_log(self, event):
        self.log_text.delete(1.0, END)

    def print_log(self, log):
        self.log_text.insert(END, log + '\n')
        self.log_text.see(END)

    def update_button_state(self, event):
        port = self.serial_port_combo.get()
        self.session = Session(port)
        self.print_log(f"Selected Serial Port: {port}")
        self.establish_button.config(state=NORMAL)
        self.get_temperature_button.config(state=DISABLED)
        self.toggle_led_button.config(state=DISABLED)

def list_serial_ports():
    ports = comports()
    return [port.device for port in ports]

if __name__ == "__main__":
    root = Tk()
    combobox_options = list_serial_ports()
    app = SecureClientApp(root, combobox_options)
    root.mainloop()
