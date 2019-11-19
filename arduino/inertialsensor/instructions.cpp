#include "instructions.h"



void SET_POWER(SerialTalks& inst, Deserializer& input, Serializer& output)
{
    int led1 = 13;
    pinMode(led1,OUTPUT);

    if(!input.read<byte>()){
        digitalWrite(led1,true);
    }else{
        digitalWrite(led1,false);
    }
}

void ACQUIRE_DATA(SerialTalks& inst, Deserializer& input, Serializer& output){
    extern Adafruit_BNO055 bno;

    sensors_event_t event; 
    bno.getEvent(&event);

    output.write<float>(event.orientation.x);
    output.write<float>(event.orientation.y);
    output.write<float>(event.orientation.z);

}
