#include <Arduino.h>
#include "../common/SerialTalks.h"

#include "instructions.h"
#include "PIN.h"

Adafruit_BNO055 bno = Adafruit_BNO055(55);



void setup() {
    Serial.begin(SERIALTALKS_BAUDRATE);
    talks.begin(Serial);

    if(!bno.begin())
    {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    
    }
  
    delay(1000);
    
    bno.setExtCrystalUse(true);

    talks.bind(SET_POWER_OPCODE, SET_POWER);
    talks.bind(ACQUIRE_DATA_RX,ACQUIRE_DATA);
}

void loop() {
  talks.execute(); 
  
}


