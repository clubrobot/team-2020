#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <Arduino.h>

#include "../common/SerialTalks.h"
#include "PIN.h"
#include "../common/Wire.h"
#include "Adafruit_Sensor.h"
#include "Adafruit_BNO055.h"
#include "utility/imumaths.h"



// Opcodes declaration

#define SET_POWER_OPCODE 0x10
#define ACQUIRE_DATA_RX 0x11



// Instructions prototypes

void SET_POWER(SerialTalks& inst, Deserializer& input, Serializer& output);
void ACQUIRE_DATA(SerialTalks& inst, Deserializer& input, Serializer& output);


#endif






