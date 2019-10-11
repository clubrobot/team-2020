#include "VL53L0X.h"
#include <iostream>

using namespace std;

#define VERSION_REQUIRED_MAJOR 1 ///< Required sensor major version
#define VERSION_REQUIRED_MINOR 0 ///< Required sensor minor version
#define VERSION_REQUIRED_BUILD 1 ///< Required sensor build

#define STR_HELPER(x) #x     ///< a string helper
#define STR(x) STR_HELPER(x) ///< string helper wrapper

VL53L0X::VL53L0X(uint8_t i2c_addr, uint8_t shutdown_pin, uint8_t device_mode)
{
    _i2c_addr = i2c_addr;
    _shutdown_pin = shutdown_pin;
    _device_mode = device_mode;

    /* disable sensor by default to avoid multiple sensor with same adress at the begining */
    pinMode(_shutdown_pin, OUTPUT);
    digitalWrite(_shutdown_pin, LOW);
}

bool VL53L0X::begin()
{
    int32_t status_int;
    int32_t init_done = 0;

    uint32_t refSpadCount;
    uint8_t isApertureSpads;
    uint8_t VhvSettings;
    uint8_t PhaseCal;

    // Initialize Comms
    pMyDevice->I2cDevAddr = VL53L0X_I2C_ADDR; // default
    pMyDevice->comms_type = 1;
    pMyDevice->comms_speed_khz = 400;

    _Status = VL53L0X_DataInit(&MyDevice); // Data initialization

    if (!setAddress(_i2c_addr, _shutdown_pin))
    {
        return false;
    }

    _Status = VL53L0X_GetDeviceInfo(&MyDevice, &DeviceInfo);

    if (_Status == VL53L0X_ERROR_NONE)
    {
        cout << "VL53L0X Info:" << endl;
        cout << "Device Name: " << DeviceInfo.Name;
        cout << ", Type: " << DeviceInfo.Type;
        cout << ", ID: " << DeviceInfo.ProductId << endl;
        cout << "Rev Major: " << DeviceInfo.ProductRevisionMajor;
        cout << ", Minor: " << DeviceInfo.ProductRevisionMinor << endl;

        if ((DeviceInfo.ProductRevisionMinor != 1) && (DeviceInfo.ProductRevisionMinor != 1))
        {
            cout << "Error expected cut 1.1 but found ";
            cout << DeviceInfo.ProductRevisionMajor;
            cout << ',';
            cout << DeviceInfo.ProductRevisionMinor << endl;
        }

        _Status = VL53L0X_ERROR_NOT_SUPPORTED;
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        cout << "VL53L0X: StaticInit" << endl;

        _Status = VL53L0X_StaticInit(pMyDevice); // Device Initialization
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        cout << "VL53L0X: PerformRefSpadManagement" << endl;

        _Status = VL53L0X_PerformRefSpadManagement(pMyDevice, &refSpadCount, &isApertureSpads); // Device Initialization

        cout << "refSpadCount = " << refSpadCount;
        cout << ", isApertureSpads = " << isApertureSpads << endl;
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        cout << "VL53L0X: PerformRefCalibration" << endl;

        _Status = VL53L0X_PerformRefCalibration(pMyDevice, &VhvSettings, &PhaseCal); // Device Initialization
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        cout << "VL53L0X: SetDeviceMode" << endl;

        _Status = VL53L0X_SetDeviceMode(pMyDevice, _device_mode);
    }

    // Enable/Disable Sigma and Signal check
    if (_Status == VL53L0X_ERROR_NONE)
    {
        _Status = VL53L0X_SetLimitCheckEnable(pMyDevice, VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE, 1);
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        _Status = VL53L0X_SetLimitCheckEnable(pMyDevice, VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE, 1);
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        _Status = VL53L0X_SetLimitCheckEnable(pMyDevice, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, 1);
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        _Status = VL53L0X_SetLimitCheckValue(pMyDevice, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, (FixPoint1616_t)(1.5 * 0.023 * 65536));
    }

    if (_Status == VL53L0X_ERROR_NONE)
    {
        return true;
    }
    else
    {
        cout << "VL53L0X Error: " << _Status << endl;
        return false;
    }
}

/**************************************************************************/
/*!
    @brief  Change the I2C address of the sensor
    @param  newAddr the new address to set the sensor to
    @returns True if address was set successfully, False otherwise
*/
/**************************************************************************/
boolean VL53L0X::setAddress(uint8_t newAddr, uint8_t shutdown_pin)
{
    newAddr &= 0x7F;

    // init desired sensor
    pinMode(shutdown_pin, INPUT);
    delay(2); // Not ideal but we need to wait for the sensors to boot

    _Status = VL53L0X_SetDeviceAddress(pMyDevice, newAddr * 2); // 7->8 bit

    delay(10);

    if (_Status == VL53L0X_ERROR_NONE)
    {
        pMyDevice->I2cDevAddr = newAddr; // 7 bit addr
        return true;
    }
    return false;
}