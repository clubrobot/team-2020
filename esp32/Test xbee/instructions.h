#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <Arduino.h>

#include "../../arduino/common/SerialTalks.h"
#include "PIN.h"
#include "../../arduino/common/Wire.h"


// Opcodes declaration

#define TEST_CO_I2C 0x11
#define ACQUIRE_DATA_RX 0x12
#define CALIBRATION_CODE 0x13



// Instructions prototypes

void TEST_CONNECTION(SerialTalks& inst, Deserializer& input, Serializer& output);
void ACQUIRE_DATA(SerialTalks& inst, Deserializer& input, Serializer& output);
void GET_CALIBRATION(SerialTalks& inst, Deserializer& input, Serializer& output);


#endif






