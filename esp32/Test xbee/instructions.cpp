#include "instructions.h"



void TEST_CONNECTION(SerialTalks& inst, Deserializer& input, Serializer& output){
    extern int MPU;
    int connection = 0;
    Wire.begin();                      // Initialize comunication
    Wire.beginTransmission(MPU);       // Start communication with MPU6050 // MPU=0x68
    if(Wire.write(0x6B)){                // Talk to the register 6B
        Wire.write(0x00);                  // Make reset - place a 0 into the 6B register
        Wire.endTransmission(true);        //end the transmission

        connection = 1;
    }
    
    output.write<int>(connection);

}

void ACQUIRE_DATA(SerialTalks& inst, Deserializer& input, Serializer& output){    
    extern int MPU;
    float AccX, AccY, AccZ;
    float GyroX, GyroY, GyroZ;

    Wire.beginTransmission(MPU);
    Wire.write(0x3B); // Start with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 6 registers total, each axis value is stored in 2 registers
    //For a range of +-8g, we need to divide the raw values by 4096, according to the datasheet
    AccX = (Wire.read() << 8 | Wire.read()) / 4096.0; // X-axis value
    AccY = (Wire.read() << 8 | Wire.read()) / 4096.0; // Y-axis value
    
    // === Read gyroscope data === //
    Wire.beginTransmission(MPU);
    Wire.write(0x47); // Gyro data Z register address 0x47
    Wire.endTransmission(false);
    Wire.requestFrom(MPU, 6, true); // Read 4 registers total, each axis value is stored in 2 registers
// For a 250deg/s range we have to divide first the raw value by 131.0, according to the datasheet

    GyroZ = (Wire.read() << 8 | Wire.read()) / 131.0;
    
    output.write<float>(AccX);
    output.write<float>(AccY);
    output.write<float>(GyroZ);

}

void GET_CALIBRATION(SerialTalks& inst, Deserializer& input, Serializer& output){    
    extern int MPU;
    float AccX, AccY, AccZ;
    float GyroX, GyroY, GyroZ;
    float AccErrorX =0, AccErrorY=0, AccErrorZ=0, GyroErrorX=0, GyroErrorY=0, GyroErrorZ=0;

    int c = 0;

    // We can call this funtion in the setup section to calculate the accelerometer and gyro data error. From here we will get the error values used in the above equations printed on the Serial Monitor.
  // Note that we should place the IMU flat in order to get the proper values, so that we then can the correct values
  // Read accelerometer values 200 times
    while (c < 200) {
        Wire.beginTransmission(MPU);
        Wire.write(0x3B);
        Wire.endTransmission(false);
        Wire.requestFrom(MPU, 6, true);
        AccX = (Wire.read() << 8 | Wire.read()) / 4096.0 ;
        AccY = (Wire.read() << 8 | Wire.read()) / 4096.0 ;
        AccZ = (Wire.read() << 8 | Wire.read()) / 4096.0 ;
        // Sum all readings
        /*AccErrorX = AccErrorX + ((atan((AccY) / sqrt(pow((AccX), 2) + pow((AccZ), 2))) * 180 / PI));
        AccErrorY = AccErrorY + ((atan(-1 * (AccX) / sqrt(pow((AccY), 2) + pow((AccZ), 2))) * 180 / PI));*/
        AccErrorX = AccErrorX + AccX;
        AccErrorY = AccErrorY + AccY;
        AccErrorZ = AccErrorZ + AccZ;
        c++;
    }
    //Divide the sum by 200 to get the error value
    AccErrorX = AccErrorX / 200;
    AccErrorY = AccErrorY / 200;
    AccErrorZ = AccErrorZ / 200;

    c = 0;
    // Read gyro values 200 times
    while (c < 200) {
        Wire.beginTransmission(MPU);
        Wire.write(0x43);
        Wire.endTransmission(false);
        Wire.requestFrom(MPU, 6, true);
        GyroX = Wire.read() << 8 | Wire.read();
        GyroY = Wire.read() << 8 | Wire.read();
        GyroZ = Wire.read() << 8 | Wire.read();
        // Sum all readings
        GyroErrorX = GyroErrorX + (GyroX / 131.0);
        GyroErrorY = GyroErrorY + (GyroY / 131.0);
        GyroErrorZ = GyroErrorZ + (GyroZ / 131.0);
        c++;
    }
    //Divide the sum by 200 to get the error value
    GyroErrorX = GyroErrorX / 200;
    GyroErrorY = GyroErrorY / 200;
    GyroErrorZ = GyroErrorZ / 200;
   
    output.write<float>(AccErrorX);
    output.write<float>(AccErrorY);
    output.write<float>(AccErrorZ);
    output.write<float>(GyroErrorX); 
    output.write<float>(GyroErrorY);
    output.write<float>(GyroErrorZ);



}