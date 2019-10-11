#include <Arduino.h>
#include <Wire.h>
#include <SerialTalks.h>
#include "instructions.h"

void setup()
{
    Wire.begin();

    //Starting SerialTalks
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
}
void loop()
{
    talks.execute();
}