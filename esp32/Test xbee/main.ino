#include "instructions.h"

int MPU = 0x68; // MPU6050 I2C address

void setup() {
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    talks.bind(TEST_CO_I2C,TEST_CONNECTION);
    talks.bind(ACQUIRE_DATA_RX,ACQUIRE_DATA);
    talks.bind(CALIBRATION_CODE,GET_CALIBRATION);

}

void loop() {
  talks.execute(); 
  
}


