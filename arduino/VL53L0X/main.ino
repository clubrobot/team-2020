#include <Arduino.h>
#include <Wire.h>
#include "../common/VL53L0X.h"

VL53L0X s1 = VL53L0X(0X44, 11);
VL53L0X s2 = VL53L0X(0X45, 6);
void setup()
{
    pinMode(7, OUTPUT);
    digitalWrite(7, HIGH);

    Wire.begin();

    Serial.begin(115200);

    s1.shutdown();
    s2.shutdown();

    if (!s1.begin())
    {
        Serial.println("failedToBoot");
    }
    if (!s2.begin())
    {
        Serial.println("failedToBoot");
    }

    s1.setTimeout(30);
    s2.setTimeout(30);

    s1.startContinuous();
    s2.startContinuous();
}

void loop()
{
    Serial.println(s1.readRangeContinuousMillimeters());
    Serial.println(s2.readRangeContinuousMillimeters());
}
