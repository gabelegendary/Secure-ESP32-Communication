#include "serial_communication.h"
#include <Arduino.h>

#define BAUDRATE 115200

bool initialize_serial()
{
    Serial.begin(BAUDRATE);
    return Serial;
}

bool send_data(const uint8_t *data, size_t dlen)
{
    return (dlen == Serial.write(data, dlen));
}

size_t receive_data(uint8_t *buf, size_t blen)
{
    if (Serial.available() > 0)
    {
        return Serial.readBytes(buf, blen);
    }
    return 0;
}

void close_serial()
{
    Serial.end();
}
