#ifndef VL53L0X_H
#define VL53L0X_H

#include <Arduino.h>

#include "vl53l0x_api.h"

#define VL53L0X_I2C_ADDR 0x29 /* Default sensor I2C address */

class VL53L0X
{
public:
    VL53L0X(TwoWire &i2c, uint8_t i2c_addr = VL53L0X_I2C_ADDR, uint8_t shutdown_pin = NULL, uint8_t device_mode = VL53L0X_DEVICEMODE_SINGLE_RANGING);

    bool begin();

    VL53L0X_Error getSingleRangingMeasurement(VL53L0X_RangingMeasurementData_t *pRangingMeasurementData);
    VL53L0X_Error getContinuousRangingMeasurement(VL53L0X_RangingMeasurementData_t *pRangingMeasurementData);

private:
    bool setAddress(uint8_t newAddr, uint8_t shutdown_pin);
    void printRangeStatus(VL53L0X_RangingMeasurementData_t *pRangingMeasurementData);

    VL53L0X_Error _Status = VL53L0X_ERROR_NONE;

    VL53L0X_Dev_t MyDevice;
    VL53L0X_Version_t Version;
    VL53L0X_DeviceInfo_t DeviceInfo;

    uint8_t _i2c_addr;
    uint8_t _shutdown_pin;
    uint8_t _device_mode;
};

#endif