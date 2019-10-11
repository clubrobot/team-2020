#include "VL53L0X.h"
#include <iostream>

using namespace std;

#define VERSION_REQUIRED_MAJOR 1 ///< Required sensor major version
#define VERSION_REQUIRED_MINOR 0 ///< Required sensor minor version
#define VERSION_REQUIRED_BUILD 1 ///< Required sensor build

#define STR_HELPER(x) #x     ///< a string helper
#define STR(x) STR_HELPER(x) ///< string helper wrapper

/**
 * @brief Construct a new VL53L0X::VL53L0X object
 *
 * @param i2c
 * @param i2c_addr
 * @param shutdown_pin
 * @param device_mode
 */
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
/**
 * @brief
 *
 * @return true
 * @return false
 */
bool VL53L0X::begin()
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    int32_t status_int;
    int32_t init_done = 0;

    uint32_t refSpadCount;
    uint8_t isApertureSpads;
    uint8_t VhvSettings;
    uint8_t PhaseCal;

    Status = VL53L0X_DataInit(&_device); // Data initialization

    if (!setAddress(_i2c_addr, _shutdown_pin))
    {
        return false;
    }

    Status = VL53L0X_GetDeviceInfo(&_device, &_deviceInfo);

#ifdef VL53L0X_LOG
    if (Status == VL53L0X_ERROR_NONE)
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

        Status = VL53L0X_ERROR_NOT_SUPPORTED;
    }
#endif

    if (Status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: StaticInit" << endl;
#endif
        Status = VL53L0X_StaticInit(&_device); // Device Initialization
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: PerformRefSpadManagement" << endl;
#endif
        Status = VL53L0X_PerformRefSpadManagement(&_device, &refSpadCount, &isApertureSpads); // Device Initialization
#ifdef VL53L0X_LOG
        cout << "refSpadCount = " << refSpadCount;
        cout << ", isApertureSpads = " << isApertureSpads << endl;
#endif
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: PerformRefCalibration" << endl;
#endif
        Status = VL53L0X_PerformRefCalibration(&_device, &VhvSettings, &PhaseCal); // Device Initialization
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X: SetDeviceMode" << endl;
#endif
        Status = VL53L0X_SetDeviceMode(&_device, _device_mode);
    }

    // Enable/Disable Sigma and Signal check
    if (Status == VL53L0X_ERROR_NONE)
    {
        Status = VL53L0X_SetLimitCheckEnable(&_device, VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE, 1);
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
        Status = VL53L0X_SetLimitCheckEnable(&_device, VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE, 1);
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
        Status = VL53L0X_SetLimitCheckEnable(&_device, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, 1);
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
        Status = VL53L0X_SetLimitCheckValue(&_device, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, (FixPoint1616_t)(1.5 * 0.023 * 65536));
    }

    switch (_device_mode)
    {
    case VL53L0X_DEVICEMODE_SINGLE_RANGING:
        break;
    case VL53L0X_DEVICEMODE_CONTINUOUS_RANGING:
        //Status = VL53L0X_StartMeasurement(&_device);
        // #ifdef VL53L0X_LOG
        //         if (Status != VL53L0X_ERROR_NONE)
        //         {
        //             cout << "Error while starting Continuous mesurement : " << Status << endl;
        //         }
        // #endif
        //break;
    case VL53L0X_DEVICEMODE_CONTINUOUS_TIMED_RANGING:
    case VL53L0X_DEVICEMODE_SINGLE_HISTOGRAM:
    case VL53L0X_DEVICEMODE_SINGLE_ALS:
    case VL53L0X_DEVICEMODE_GPIO_DRIVE:
    case VL53L0X_DEVICEMODE_GPIO_OSC:
    default:
#ifdef VL53L0X_LOG
        cout << "Unsuported mode " << endl;
#endif
        return false;
        break;
    }

    if (Status == VL53L0X_ERROR_NONE)
    {
        return true;
    }
    else
    {
#ifdef VL53L0X_LOG
        cout << "VL53L0X Error: " << Status << endl;
#endif
        return false;
    }
}
/**
 * @brief
 *
 * @param pRangingMeasurementData
 * @return VL53L0X_Error
 */
VL53L0X_Error VL53L0X::getRangingMeasurement(VL53L0X_RangingMeasurementData_t *pRangingMeasurementData)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    FixPoint1616_t LimitCheckCurrent;

    switch (_device_mode)
    {
    case VL53L0X_DEVICEMODE_SINGLE_RANGING:
        Status = getSingleRangingMeasurement(pRangingMeasurementData);
        break;
    case VL53L0X_DEVICEMODE_CONTINUOUS_RANGING:
        // Status = getContinuousRangingMeasurement(pRangingMeasurementData);
        // break;
    case VL53L0X_DEVICEMODE_CONTINUOUS_TIMED_RANGING:
    case VL53L0X_DEVICEMODE_SINGLE_HISTOGRAM:
    case VL53L0X_DEVICEMODE_SINGLE_ALS:
    case VL53L0X_DEVICEMODE_GPIO_DRIVE:
    case VL53L0X_DEVICEMODE_GPIO_OSC:
    default:
#ifdef VL53L0X_LOG
        cout << "Unsuported mode " << endl;
#endif
        Status = VL53L0X_ERROR_MODE_NOT_SUPPORTED;
        break;
    }

#ifdef VL53L0X_LOG
    printRangeStatus(pRangingMeasurementData);

    VL53L0X_GetLimitCheckCurrent(&_device, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, &LimitCheckCurrent);

    cout << "RANGE IGNORE THRESHOLD: " << (float)(LimitCheckCurrent / 65536.0) << endl;

    cout << "Measured distance: " << pRangingMeasurementData->RangeMilliMeter << endl;
#endif
    return Status;
}
/**
 * @brief
 *
 * @param RangingMeasurementData
 * @return VL53L0X_Error
 */
VL53L0X_Error VL53L0X::getSingleRangingMeasurement(VL53L0X_RangingMeasurementData_t *RangingMeasurementData)
{
#ifdef VL53L0X_LOG
    cout << "sVL53L0X: PerformSingleRangingMeasurement" << endl;
#endif
    return VL53L0X_PerformSingleRangingMeasurement(&_device, RangingMeasurementData);
}
/**
 * @brief
 *
 * @param pRangingMeasurementData
 * @return VL53L0X_Error
 */
VL53L0X_Error VL53L0X::getContinuousRangingMeasurement(VL53L0X_RangingMeasurementData_t *pRangingMeasurementData)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;

#ifdef VL53L0X_LOG
    cout << "sVL53L0X: PerformContinuousRangingMeasurement" << endl;
#endif
    Status = WaitMeasurementDataReady(&_device);

    if (Status == VL53L0X_ERROR_NONE)
    {
        Status = VL53L0X_GetRangingMeasurementData(&_device, pRangingMeasurementData);

        // Clear the interrupt
        VL53L0X_ClearInterruptMask(&_device, VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_NEW_SAMPLE_READY);
    }
    return Status;
}
/**
 * @brief
 *
 * @param Dev
 * @return VL53L0X_Error
 */
VL53L0X_Error VL53L0X::WaitMeasurementDataReady(VL53L0X_DEV Dev)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    uint8_t NewDatReady = 0;
    uint32_t LoopNb;

    // Wait until it finished
    // use timeout to avoid deadlock
    if (Status == VL53L0X_ERROR_NONE)
    {
        LoopNb = 0;
        do
        {
            Status = VL53L0X_GetMeasurementDataReady(Dev, &NewDatReady);
            if ((NewDatReady == 0x01) || Status != VL53L0X_ERROR_NONE)
            {
                break;
            }
            LoopNb = LoopNb + 1;
            VL53L0X_PollingDelay(Dev);
        } while (LoopNb < VL53L0X_DEFAULT_MAX_LOOP);

        if (LoopNb >= VL53L0X_DEFAULT_MAX_LOOP)
        {
            Status = VL53L0X_ERROR_TIME_OUT;
        }
    }

    return Status;
}
/**
 * @brief
 *
 * @param newAddr
 * @param shutdown_pin
 * @return boolean
 */
boolean VL53L0X::setAddress(uint8_t newAddr, uint8_t shutdown_pin)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    newAddr &= 0x7F;

    // Enable sensor
    pinMode(shutdown_pin, INPUT);
    delay(2); // Not ideal but we need to wait for the sensors to boot

    Status = VL53L0X_SetDeviceAddress(&_device, newAddr * 2); // 7->8 bit

    delay(10);

    if (Status == VL53L0X_ERROR_NONE)
    {
        _device.I2cDevAddr = newAddr; // 7 bit addr
        return true;
    }
    return false;
}
/**
 * @brief
 *
 * @param pRangingMeasurementData
 */
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