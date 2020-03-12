#include "xbee.h"


void setup() {
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);
    pinMode(2,OUTPUT);

    message();

    /*talks.bind(TEST_CO_I2C,TEST_CONNECTION);
    talks.bind(ACQUIRE_DATA_RX,ACQUIRE_DATA);
    talks.bind(CALIBRATION_CODE,GET_CALIBRATION);*/

}

void loop() {
  talks.execute();

  digitalWrite(2,HIGH); 
  
}

