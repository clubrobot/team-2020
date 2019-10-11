#include <Arduino.h>
#include <Wire.h>
#include <SerialTalks.h>
#include <TaskManager.h>
#include <VL53L0X.h>
#include "instructions.h"

TaskManager tm;

TickType_t xDelay = 1000 / portTICK_PERIOD_MS; // 1000 ms task Delay

VL53L0X sensor1(Wire, 0x30);
VL53L0X sensor2(Wire, 0x31);

static VL53L0X_RangingMeasurementData_t dataSensor1;
static VL53L0X_RangingMeasurementData_t dataSensor2;

void loop_aux(void *aux);

void setup()
{
    Wire.begin();

    //Starting SerialTalks
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    if (!sensor1.begin())
    {
        Serial.println("Sensor 1 init error");
    }
    if (!sensor2.begin())
    {
        Serial.println("Sensor 1 init error");
    }

    tm.create_task(loop_aux, NULL);
}
void loop()
{
    talks.execute();
}

void loop_aux(void *aux)
{
    for (;;)
    {
        if (sensor1.getSingleRangingMeasurement(&dataSensor1) == VL53L0X_ERROR_NONE)
        {
            Serial.println("Sensor 1 success");
        }
        else
        {
            Serial.println("Sensor 1 error");
        }

        if (sensor2.getSingleRangingMeasurement(&dataSensor2) == VL53L0X_ERROR_NONE)
        {
            Serial.println("Sensor 2 success");
        }
        else
        {
            Serial.println("Sensor 2 error");
        }

        vTaskDelay(xDelay);
    }
}