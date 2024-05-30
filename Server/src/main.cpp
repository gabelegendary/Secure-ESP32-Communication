#include <Arduino.h>
#include <driver/adc.h>
#include <esp_adc_cal.h>

const int ledPin = 21;
bool ledState = LOW;

extern "C" uint8_t temprature_sens_read();

float readInternalTemperature()
{
  uint8_t temp_raw = temprature_sens_read();
  return (temp_raw - 32) / 1.8;
}

void setup()
{
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  Serial.println("Setup completed.");
}

void toggleLED()
{
  ledState = !ledState;
  digitalWrite(ledPin, ledState);
}

void loop()
{
  static String command = "";
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == '\n')
    {
      command.trim();
      if (command == "T")
      {
        toggleLED();
        Serial.println("LED toggled.");
      }
      else if (command == "temp")
      {
        float temp_celsius = readInternalTemperature();
        Serial.print("Internal Temperature: ");
        Serial.print(temp_celsius);
        Serial.println(" °C");
        Serial.println("Temperature data sent.");
      }
      else
      {
        Serial.println("Invalid command received.");
      }
      command = "";
    }
    else
    {
      command += c;
    }
  }
}
