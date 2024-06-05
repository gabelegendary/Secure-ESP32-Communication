#include <Arduino.h>
#include <driver/adc.h>
#include <esp_adc_cal.h>
#include "session.h"
#include "serial_communication.h"

const int ledPin = 21; // Define the pin for the LED
bool ledState = LOW;   // Initial state of the LED

void setup()
{
  pinMode(ledPin, OUTPUT); // Initialize the LED pin as an output
  Serial.begin(115200);    // Start serial communication at 115200 baud
  Serial.println("Setup completed.");
  session_init(); // Initialize the session for key exchange
  delay(1000);    // Give some time for initialization
}

void toggleLED()
{
  ledState = !ledState;           // Toggle the LED state
  digitalWrite(ledPin, ledState); // Write the LED state to the pin
  Serial.println("LED toggled.");
}

void loop()
{
  uint8_t command[64];                                    // Buffer to hold incoming data
  size_t length = receive_data(command, sizeof(command)); // Receive data

  if (length > 0)
  {
    Serial.print("Command received: ");
    Serial.println(command[0], HEX);

    switch (command[0])
    {
    case 0x01: // Command for toggling LED
      toggleLED();
      break;
    case 0x02: // Command for getting temperature
    {
      float temp_celsius = temperatureRead();
      send_data((uint8_t *)&temp_celsius, sizeof(temp_celsius));
      Serial.println("Temperature sent.");
      break;
    }
    case 0x03: // Command for key exchange
      Serial.println("Key exchange command received.");
      server_receive_and_verify_key();
      break;
    default:
      Serial.println("Invalid command received.");
      break;
    }
  }
}
