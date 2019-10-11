#include "VL53L0X.h"
#include <iostream>

using namespace std;

#define VERSION_REQUIRED_MAJOR 1 ///< Required sensor major version
#define VERSION_REQUIRED_MINOR 0 ///< Required sensor minor version
#define VERSION_REQUIRED_BUILD 1 ///< Required sensor build

#define STR_HELPER(x) #x     ///< a string helper
#define STR(x) STR_HELPER(x) ///< string helper wrapper

VL53L0X::VL53L0X(TwoWire &i2c, uint8_t i2c_addr, uint8_t shutdown_pin, uint8_t device_mode)
{

    // Initialize Comms
    _device.I2cDevAddr = VL53L0X_I2C_ADDR; // default
    _device.comms_type = 1;
    _device.comms_speed_khz = 400;
    _device.i2c = &i2c;

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

    _status = VL53L0X_DataInit(&_device); // Data initialization

    if (!setAddress(_i2c_addr, _shutdown_pin))
    {
        return false;
    }

    _status = VL53L0X_GetDeviceInfo(&_device, &_deviceInfo);

#ifdef VL53L0X_LOG
    if (_status == VL53L0X_ERROR_NONE)
    {
        cout << "VL53L0X Info:" << endl;
        cout << "Device Name: " << _deviceInfo.Name;
        cout << ", Type: " << _deviceInfo.Type;
        cout << ", ID: " << _deviceInfo.ProductId << endl;
        cout << "Rev Major: " << _deviceInfo.ProductRevisionMajor;
        cout << ", Minor: " << _deviceInfo.ProductRevisionMinor << endl;

        if ((_deviceInfo.ProductRevisionMinor != 1) && (_deviceInfo.ProductRevisionMinor != 1))
        {
            cout << "Error expected cut 1.1 but found ";
            cout << _deviceInfo.ProductRevisionMajor;
            cout << ',';
            cout << _deviceInfo.ProductRevisionMinor << endl;
        }

        _status = VL53L0X_ERROR_NOT_SUPPORTED;
    }
#endif

    if (_status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: StaticInit" << endl;
#endif
        _status = VL53L0X_StaticInit(&_device); // Device Initialization
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: PerformRefSpadManagement" << endl;
#endif
        _status = VL53L0X_PerformRefSpadManagement(&_device, &refSpadCount, &isApertureSpads); // Device Initialization
#ifdef VL53L0X_LOG
        cout << "refSpadCount = " << refSpadCount;
        cout << ", isApertureSpads = " << isApertureSpads << endl;
#endif
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: PerformRefCalibration" << endl;
#endif
        _status = VL53L0X_PerformRefCalibration(&_device, &VhvSettings, &PhaseCal); // Device Initialization
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: SetDeviceMode" << endl;
#endif
        _status = VL53L0X_SetDeviceMode(&_device, _device_mode);
    }

    // Enable/Disable Sigma and Signal check
    if (_status == VL53L0X_ERROR_NONE)
    {
        _status = VL53L0X_SetLimitCheckEnable(&_device, VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE, 1);
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
        _status = VL53L0X_SetLimitCheckEnable(&_device, VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE, 1);
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
        _status = VL53L0X_SetLimitCheckEnable(&_device, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, 1);
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
        _status = VL53L0X_SetLimitCheckValue(&_device, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, (FixPoint1616_t)(1.5 * 0.023 * 65536));
    }

    if (_status == VL53L0X_ERROR_NONE)
    {
        return true;
    }
    else
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X Error: " << _status << endl;
#endif
        return false;
    }
}

boolean VL53L0X::setAddress(uint8_t newAddr, uint8_t shutdown_pin)
{
    newAddr &= 0x7F;

    // init desired sensor
    pinMode(shutdown_pin, INPUT);
    delay(2); // Not ideal but we need to wait for the sensors to boot

    _status = VL53L0X_SetDeviceAddress(&_device, newAddr * 2); // 7->8 bit

    delay(10);

    if (_status == VL53L0X_ERROR_NONE)
    {
        _device.I2cDevAddr = newAddr; // 7 bit addr
        return true;
    }
    return false;
}

VL53L0X_Error VL53L0X::getSingleRangingMeasurement(VL53L0X_RangingMeasurementData_t *RangingMeasurementData)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    FixPoint1616_t LimitCheckCurrent;

    /*
     *  Step  4 : Test ranging mode
     */

    if (Status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        Serial.println(F("sVL53L0X: PerformSingleRangingMeasurement"));
#endif
        Status = VL53L0X_PerformSingleRangingMeasurement(&_device, RangingMeasurementData);

#ifdef VL53L0X_LOG
        printRangeStatus(RangingMeasurementData);

        VL53L0X_GetLimitCheckCurrent(&_device, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, &LimitCheckCurrent);

        Serial.print(F("RANGE IGNORE THRESHOLD: "));
        Serial.println((float)LimitCheckCurrent / 65536.0);

        Serial.print(F("Measured distance: "));
        Serial.println(RangingMeasurementData->RangeMilliMeter);
#endif
    }
    return Status;
}

void VL53L0X::printRangeStatus(VL53L0X_RangingMeasurementData_t *pRangingMeasurementData)
{
    char buf[VL53L0X_MAX_STRING_LENGTH];
    uint8_t RangeStatus;

    /*
     * New Range Status: data is valid when pRangingMeasurementData->RangeStatus = 0
     */

    RangeStatus = pRangingMeasurementData->RangeStatus;

    VL53L0X_GetRangeStatusString(RangeStatus, buf);

    cout << "Range Status: " << RangeStatus << " : " << buf << endl;
}