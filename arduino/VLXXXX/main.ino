#include <Arduino.h>
#include <Wire.h>
#include "../common/VL53L0X.h"
#include "../common/VL6180X.h"

VL53L0X s1 = VL53L0X(0X44, 11);
VL53L0X s2 = VL53L0X(0X45, 6);

VL6180X s3 = VL6180X(0X46, 10);
VL6180X s4 = VL6180X(0X48, 5);

void setup()
{
    pinMode(7, OUTPUT);
    digitalWrite(7, HIGH);

    Wire.begin();

    Serial.begin(115200);

    s1.shutdown();
    s2.shutdown();
    s3.shutdown();
    s4.shutdown();

    if (!s1.begin())
    {
        Serial.println("failedToBoot");
    }
    if (!s2.begin())
    {
        Serial.println("failedToBoot");
    }
    if (!s3.begin())
    {
        Serial.println("failedToBoot");
    }
    if (!s4.begin())
    {
        Serial.println("failedToBoot");
    }

    s1.setTimeout(30);
    s2.setTimeout(30);
    s3.setTimeout(30);
    s4.setTimeout(30);

    s3.configureDefault();
    s4.configureDefault();

    s1.startContinuous();
    s2.startContinuous();
    s3.startRangeContinuous(60);
    s4.startRangeContinuous(60);
}

void loop()
{
    // Serial.println(s1.readRangeContinuousMillimeters());
    // Serial.println(s2.readRangeContinuousMillimeters());
    Serial.println(s3.readRangeContinuousMillimeters());
    //Serial.println(s4.readRangeContinuousMillimeters());
}
