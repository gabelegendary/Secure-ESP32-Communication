#include <Arduino.h>
#include <esp_system.h>
#include "serial_communication.h"

// Define the pin for the LED
const int ledPin = 21;

// Define command constants
const uint8_t GET_TEMPERATURE = 0x01;
const uint8_t TOGGLE_LED = 0x02;

void setup()
{
  // Initialize serial communication at the defined baud rate
  initialize_serial();

  // Initialize the LED pin as an output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop()
{
  // Buffer to hold incoming data
  uint8_t buffer[64];
  size_t len = receive_data(buffer, sizeof(buffer));

  // If data is received
  if (len == 1)
  {
    switch (buffer[0])
    {
    case GET_TEMPERATURE:
    {
      float temperature = temperatureRead();
      send_data((uint8_t *)&temperature, sizeof(temperature));
    }
    break;

    case TOGGLE_LED:
    {
      digitalWrite(ledPin, !digitalRead(ledPin));
      uint8_t response[1] = {TOGGLE_LED};
      send_data(response, 1);
    }
    break;

    default:
      // Handle unrecognized command
      send_data((uint8_t *)"Unknown command.", 16);
      break;
    }
  }
}
