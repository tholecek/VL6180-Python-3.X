#!/usr/bin/python
# Supports Python 3.X and Above

import time
import smbus

# ===========================================================================
# ST_VL6180x ToF ranger Class
#
# Code updated to Python 3.X by T. Holecek
# References ST_VL6180x Repository of A, Weber
# https://bitbucket.org/310weber/st_vl6180x
#
# Originally written by A. Weber
# References Arduino library by Casey Kuhns of SparkFun:
# https://github.com/sparkfun/ToF_Range_Finder-VL6180_Library\
# ===========================================================================


class VL6180X:
    i2c = None

    __VL6180X_IDENTIFICATION_MODEL_ID               = 0x0000
    __VL6180X_IDENTIFICATION_MODEL_REV_MAJOR        = 0x0001
    __VL6180X_IDENTIFICATION_MODEL_REV_MINOR        = 0x0002
    __VL6180X_IDENTIFICATION_MODULE_REV_MAJOR       = 0x0003
    __VL6180X_IDENTIFICATION_MODULE_REV_MINOR       = 0x0004
    __VL6180X_IDENTIFICATION_DATE                   = 0x0006    # 16bit value
    __VL6180X_IDENTIFICATION_TIME                   = 0x0008    # 16bit value

    __VL6180X_SYSTEM_MODE_GPIO0                     = 0x0010
    __VL6180X_SYSTEM_MODE_GPIO1                     = 0x0011
    __VL6180X_SYSTEM_HISTORY_CTRL                   = 0x0012
    __VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO          = 0x0014
    __VL6180X_SYSTEM_INTERRUPT_CLEAR                = 0x0015
    __VL6180X_SYSTEM_FRESH_OUT_OF_RESET             = 0x0016
    __VL6180X_SYSTEM_GROUPED_PARAMETER_HOLD         = 0x0017

    __VL6180X_SYSRANGE_START                        = 0x0018
    __VL6180X_SYSRANGE_THRESH_HIGH                  = 0x0019
    __VL6180X_SYSRANGE_THRESH_LOW                   = 0x001A
    __VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD      = 0x001B
    __VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME         = 0x001C
    __VL6180X_SYSRANGE_CROSSTALK_COMPENSATION_RATE  = 0x001E
    __VL6180X_SYSRANGE_CROSSTALK_VALID_HEIGHT       = 0x0021
    __VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE   = 0x0022
    __VL6180X_SYSRANGE_PART_TO_PART_RANGE_OFFSET    = 0x0024
    __VL6180X_SYSRANGE_RANGE_IGNORE_VALID_HEIGHT    = 0x0025
    __VL6180X_SYSRANGE_RANGE_IGNORE_THRESHOLD       = 0x0026
    __VL6180X_SYSRANGE_MAX_AMBIENT_LEVEL_MULT       = 0x002C
    __VL6180X_SYSRANGE_RANGE_CHECK_ENABLES          = 0x002D
    __VL6180X_SYSRANGE_VHV_RECALIBRATE              = 0x002E
    __VL6180X_SYSRANGE_VHV_REPEAT_RATE              = 0x0031

    __VL6180X_SYSALS_START                          = 0x0038
    __VL6180X_SYSALS_THRESH_HIGH                    = 0x003A
    __VL6180X_SYSALS_THRESH_LOW                     = 0x003C
    __VL6180X_SYSALS_INTERMEASUREMENT_PERIOD        = 0x003E
    __VL6180X_SYSALS_ANALOGUE_GAIN                  = 0x003F
    __VL6180X_SYSALS_INTEGRATION_PERIOD             = 0x0040

    __VL6180X_RESULT_RANGE_STATUS                   = 0x004D
    __VL6180X_RESULT_ALS_STATUS                     = 0x004E
    __VL6180X_RESULT_INTERRUPT_STATUS_GPIO          = 0x004F
    __VL6180X_RESULT_ALS_VAL                        = 0x0050
    __VL6180X_RESULT_HISTORY_BUFFER                 = 0x0052
    __VL6180X_RESULT_RANGE_VAL                      = 0x0062
    __VL6180X_RESULT_RANGE_RAW                      = 0x0064
    __VL6180X_RESULT_RANGE_RETURN_RATE              = 0x0066
    __VL6180X_RESULT_RANGE_REFERENCE_RATE           = 0x0068
    __VL6180X_RESULT_RANGE_RETURN_SIGNAL_COUNT      = 0x006C
    __VL6180X_RESULT_RANGE_REFERENCE_SIGNAL_COUNT   = 0x0070
    __VL6180X_RESULT_RANGE_RETURN_AMB_COUNT         = 0x0074
    __VL6180X_RESULT_RANGE_REFERENCE_AMB_COUNT      = 0x0078
    __VL6180X_RESULT_RANGE_RETURN_CONV_TIME         = 0x007C
    __VL6180X_RESULT_RANGE_REFERENCE_CONV_TIME      = 0x0080

    __VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD       = 0x010A
    __VL6180X_FIRMWARE_BOOTUP                       = 0x0119
    __VL6180X_FIRMWARE_RESULT_SCALER                = 0x0120
    __VL6180X_I2C_SLAVE_DEVICE_ADDRESS              = 0x0212
    __VL6180X_INTERLEAVED_MODE_ENABLE               = 0x02A3

    __ALS_GAIN_1    = 0x06
    __ALS_GAIN_1_25 = 0x05
    __ALS_GAIN_1_67 = 0x04
    __ALS_GAIN_2_5  = 0x03
    __ALS_GAIN_5    = 0x02
    __ALS_GAIN_10   = 0x01
    __ALS_GAIN_20   = 0x00
    __ALS_GAIN_40   = 0x07

    # Dictionaries with the valid ALS gain values
    # These simplify and clean the code (avoid abuse of if/elif/else clauses)
    ALS_GAIN_REG = {
        1:      __ALS_GAIN_1,
        1.25:   __ALS_GAIN_1_25,
        1.67:   __ALS_GAIN_1_67,
        2.5:    __ALS_GAIN_2_5,
        5:      __ALS_GAIN_5,
        10:     __ALS_GAIN_10,
        20:     __ALS_GAIN_20,
        40:     __ALS_GAIN_40
    }

    ALS_GAIN_ACTUAL = {    # Data sheet shows gain values as binary list
        1:      1.01,      # Nominal gain 1;    actual gain 1.01
        1.25:   1.28,      # Nominal gain 1.25; actual gain 1.28
        1.67:   1.72,      # Nominal gain 1.67; actual gain 1.72
        2.5:    2.60,      # Nominal gain 2.5;  actual gain 2.60
        5:      5.21,      # Nominal gain 5;    actual gain 5.21
        10:     10.32,     # Nominal gain 10;   actual gain 10.32
        20:     20.00,     # Nominal gain 20;   actual gain 20
        40:     40.00,     # Nominal gain 40;   actual gain 40
    }

    def __init__(self, address=0x29, debug=False):
        # Depending on if you have an old or a new Raspberry Pi, you
        # may need to change the I2C bus.  Older Pis use SMBus 0,
        # whereas new Pis use SMBus 1.  If you see an error like:
        # 'Error accessing 0x29: Check your I2C address '
        # change the SMBus number in the initializer below!

        # setup i2c bus and SFR address
        self.i2c = smbus.SMBus(1)
        self.address = address
        self.debug = debug

        # Module identification
        self.idModel = 0x00
        self.idModelRevMajor = 0x00
        self.idModelRevMinor = 0x00
        self.idModuleRevMajor = 0x00
        self.idModuleRevMinor = 0x00
        self.idDate = 0x00
        self.idTime = 0x00

        # Print statement updated to Python 3.X
        if self.get_register(self.__VL6180X_SYSTEM_FRESH_OUT_OF_RESET) == 1:
            print("ToF sensor is ready.")
            self.ready = True
        else:
            print("ToF sensor reset failure.")
            self.ready = False

        # Required by datasheet
        # http://www.st.com/st-web-ui/static/active/en/resource/technical/document/application_note/DM00122600.pdf
        self.set_register(0x0207, 0x01)
        self.set_register(0x0208, 0x01)
        self.set_register(0x0096, 0x00)
        self.set_register(0x0097, 0xfd)
        self.set_register(0x00e3, 0x00)
        self.set_register(0x00e4, 0x04)
        self.set_register(0x00e5, 0x02)
        self.set_register(0x00e6, 0x01)
        self.set_register(0x00e7, 0x03)
        self.set_register(0x00f5, 0x02)
        self.set_register(0x00d9, 0x05)
        self.set_register(0x00db, 0xce)
        self.set_register(0x00dc, 0x03)
        self.set_register(0x00dd, 0xf8)
        self.set_register(0x009f, 0x00)
        self.set_register(0x00a3, 0x3c)
        self.set_register(0x00b7, 0x00)
        self.set_register(0x00bb, 0x3c)
        self.set_register(0x00b2, 0x09)
        self.set_register(0x00ca, 0x09)
        self.set_register(0x0198, 0x01)
        self.set_register(0x01b0, 0x17)
        self.set_register(0x01ad, 0x00)
        self.set_register(0x00ff, 0x05)
        self.set_register(0x0100, 0x05)
        self.set_register(0x0199, 0x05)
        self.set_register(0x01a6, 0x1b)
        self.set_register(0x01ac, 0x3e)
        self.set_register(0x01a7, 0x1f)
        self.set_register(0x0030, 0x00)
        
        if self.debug:
            # Print statement updated to Python 3.X
            print("Register settings:")
            print("0x0207 - ",hex(self.get_register(0x0207)))
            print("0x0208 - ",hex(self.get_register(0x0208)))
            print("0x0096 - ",hex(self.get_register(0x0096)))
            print("0x0097 - ",hex(self.get_register(0x0097)))
            print("0x00e3 - ",hex(self.get_register(0x00e3)))
            print("0x00e4 - ",hex(self.get_register(0x00e4)))
            print("0x00e5 - ",hex(self.get_register(0x00e5)))
            print("0x00e6 - ",hex(self.get_register(0x00e6)))
            print("0x00e7 - ",hex(self.get_register(0x00e7)))
            print("0x00f5 - ",hex(self.get_register(0x00f5)))
            print("0x00d9 - ",hex(self.get_register(0x00d9)))
            print("0x00db - ",hex(self.get_register(0x00db)))
            print("0x00dc - ",hex(self.get_register(0x00dc)))
            print("0x00dd - ",hex(self.get_register(0x00dd)))
            print("0x009f - ",hex(self.get_register(0x009f)))
            print("0x00a3 - ",hex(self.get_register(0x00a3)))
            print("0x00b7 - ",hex(self.get_register(0x00b7)))
            print("0x00bb - ",hex(self.get_register(0x00bb)))
            print("0x00b2 - ",hex(self.get_register(0x00b2)))
            print("0x00ca - ",hex(self.get_register(0x00ca)))
            print("0x0198 - ",hex(self.get_register(0x0198)))
            print("0x01b0 - ",hex(self.get_register(0x01b0)))
            print("0x01ad - ",hex(self.get_register(0x01ad)))
            print("0x00ff - ",hex(self.get_register(0x00ff)))
            print("0x0100 - ",hex(self.get_register(0x0100)))
            print("0x0199 - ",hex(self.get_register(0x0199)))
            print("0x01a6 - ",hex(self.get_register(0x01a6)))
            print("0x01ac - ",hex(self.get_register(0x01ac)))
            print("0x01a7 - ",hex(self.get_register(0x01a7)))
            print("0x0030 - ",hex(self.get_register(0x0030)))

    def default_settings(self):
        # Recommended settings from datasheet
        # http://www.st.com/st-web-ui/static/active/en/resource/technical/document/application_note/DM00122600.pdf
        # Set GPIO1 high when sample complete
        self.set_register(self.__VL6180X_SYSTEM_MODE_GPIO1, 0x10)
        # Set Avg sample period
        self.set_register(self.__VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD, 0x30)
        # Set the ALS gain
        self.set_register(self.__VL6180X_SYSALS_ANALOGUE_GAIN, 0x46)
        # Set auto calibration period (Max = 255)/(OFF = 0)
        self.set_register(self.__VL6180X_SYSRANGE_VHV_REPEAT_RATE, 0xFF)
        # Set ALS integration time to 100ms
        self.set_register(self.__VL6180X_SYSALS_INTEGRATION_PERIOD, 0x63)
        # perform a single temperature calibration
        self.set_register(self.__VL6180X_SYSRANGE_VHV_RECALIBRATE, 0x01)

        # Optional settings from datasheet
        # http://www.st.com/st-web-ui/static/active/en/resource/technical/document/application_note/DM00122600.pdf
        # Set default ranging inter-measurement period to 100ms
        self.set_register(self.__VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD, 0x09)
        # Set default ALS inter-measurement period to 100ms
        self.set_register(self.__VL6180X_SYSALS_INTERMEASUREMENT_PERIOD, 0x31)
        # Configures interrupt on 'New Sample Ready threshold event' 
        self.set_register(self.__VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO, 0x24)

        # Additional settings defaults from community
        self.set_register(self.__VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME, 0x32)
        self.set_register(
            self.__VL6180X_SYSRANGE_RANGE_CHECK_ENABLES, 0x10 | 0x01)
        self.set_register_16bit(
            self.__VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE, 0x7B)
        self.set_register_16bit(self.__VL6180X_SYSALS_INTEGRATION_PERIOD, 0x64)
        self.set_register(self.__VL6180X_SYSALS_ANALOGUE_GAIN, 0x40)
        self.set_register(self.__VL6180X_FIRMWARE_RESULT_SCALER, 0x01)

        # Print statement updated to Python 3.X
        if self.debug:
            print( "Default settings:")
            print( "SYSTEM_MODE_GPIO1 - ", \
                  hex(self.get_register(self.__VL6180X_SYSTEM_MODE_GPIO1)))
            print( "READOUT_AVERAGING_SAMPLE_PERIOD - ", \
                  hex(self.get_register(
                      self.__VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD)))
            print( "SYSALS_ANALOGUE_GAIN - ", \
                  hex(self.get_register(self.__VL6180X_SYSALS_ANALOGUE_GAIN)))
            print( "SYSRANGE_VHV_REPEAT_RATE - ", \
                  hex(self.get_register(self.__VL6180X_SYSRANGE_VHV_REPEAT_RATE)))
            print( "SYSALS_INTEGRATION_PERIOD - ", \
                  hex(self.get_register(self.__VL6180X_SYSALS_INTEGRATION_PERIOD)))
            print( "SYSRANGE_VHV_RECALIBRATE - ", \
                  hex(self.get_register(self.__VL6180X_SYSRANGE_VHV_RECALIBRATE)))
            print( "SYSRANGE_INTERMEASUREMENT_PERIOD - ", \
                  hex(self.get_register(
                      self.__VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD)))
            print( "SYSALS_INTERMEASUREMENT_PERIOD - ", \
                  hex(self.get_register(
                      self.__VL6180X_SYSALS_INTERMEASUREMENT_PERIOD)))
            print( "SYSTEM_INTERRUPT_CONFIG_GPIO - ", \
                  hex(self.get_register(
                      self.__VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO)))
            print( "SYSRANGE_MAX_CONVERGENCE_TIME - ", \
                  hex(self.get_register(
                      self.__VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME)))
            print( "SYSRANGE_RANGE_CHECK_ENABLES - ", \
                  hex(self.get_register(self.__VL6180X_SYSRANGE_RANGE_CHECK_ENABLES)))
            print( "SYSRANGE_EARLY_CONVERGENCE_ESTIMATE - ", \
                  hex(self.get_register_16bit(
                      self.__VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE)))
            print( "SYSALS_INTEGRATION_PERIOD - ", \
                  hex(self.get_register_16bit(
                      self.__VL6180X_SYSALS_INTEGRATION_PERIOD)))
            print( "SYSALS_ANALOGUE_GAIN - ", \
                  hex(self.get_register(self.__VL6180X_SYSALS_ANALOGUE_GAIN)))
            print( "FIRMWARE_RESULT_SCALER - ", \
                  hex(self.get_register(self.__VL6180X_FIRMWARE_RESULT_SCALER)))

    def get_identification(self):

        self.idModel = self.get_register(
            self.__VL6180X_IDENTIFICATION_MODEL_ID)
        self.idModelRevMajor = self.get_register(
            self.__VL6180X_IDENTIFICATION_MODEL_REV_MAJOR)
        self.idModelRevMinor = self.get_register(
            self.__VL6180X_IDENTIFICATION_MODEL_REV_MINOR)
        self.idModuleRevMajor = self.get_register(
            self.__VL6180X_IDENTIFICATION_MODULE_REV_MAJOR)
        self.idModuleRevMinor = self.get_register(
            self.__VL6180X_IDENTIFICATION_MODULE_REV_MINOR)

        self.idDate = self.get_register_16bit(
            self.__VL6180X_IDENTIFICATION_DATE)
        self.idTime = self.get_register_16bit(
            self.__VL6180X_IDENTIFICATION_TIME)

    def change_address(self, old_address, new_address):
        # NOTICE:  IT APPEARS THAT CHANGING THE ADDRESS IS NOT STORED IN NON-
        # VOLATILE MEMORY POWER CYCLING THE DEVICE REVERTS ADDRESS BACK TO 0X29

        if old_address == new_address:
            return old_address
        if new_address > 127:
            return old_address

        self.set_register(self.__VL6180X_I2C_SLAVE_DEVICE_ADDRESS, new_address)
        return self.get_register(self.__VL6180X_I2C_SLAVE_DEVICE_ADDRESS)

    #Print statement updated to Python 3.X
    def get_distance(self):
        # Start Single shot mode
        self.set_register(self.__VL6180X_SYSRANGE_START, 0x01)
        time.sleep(0.010)
        if self.debug:
            print( "Range status: ", \
                  hex(self.get_register(self.__VL6180X_RESULT_RANGE_STATUS) & 0xF1))
        distance = self.get_register(self.__VL6180X_RESULT_RANGE_VAL)
        self.set_register(self.__VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)
        return distance

    def get_ambient_light(self, als_gain):
        # First load in Gain we are using, do it every time in case someone
        # changes it on us.
        # Note: Upper nibble should be set to 0x4 i.e. for ALS gain
        # of 1.0 write 0x46

        # Set the ALS gain, defaults to 20.
        # If gain is in the dictionary (defined in init()) it returns the value
        # of the constant otherwise it returns the value for gain 20.
        # This saves a lot of if/elif/else code!
        # Print statement updated to Python 3.X
        if als_gain not in self.ALS_GAIN_ACTUAL:
            print( "Invalid gain setting: ",float(als_gain),".  Setting to 20.")

        als_gain_actual = self.ALS_GAIN_ACTUAL.setdefault(als_gain, 20)
        self.set_register(
            self.__VL6180X_SYSALS_ANALOGUE_GAIN,
            (0x40 | self.ALS_GAIN_REG.setdefault(als_gain, self.__ALS_GAIN_20)))

        # Start ALS Measurement
        self.set_register(self.__VL6180X_SYSALS_START, 0x01)

        time.sleep(0.100)   # give it time...

        # Retrieve the Raw ALS value from the sensor
        #Print statement updated to Python 3.X
        if self.debug:
            print( "ALS status: ", \
                  hex(self.get_register(self.__VL6180X_RESULT_ALS_STATUS)) & 0xF1)
                   
        als_raw = self.get_register_16bit(self.__VL6180X_RESULT_ALS_VAL)
        self.set_register(self.__VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)

        # Get Integration Period for calculation, we do this every time in case
        # someone changes it on us.
        als_integration_period_raw = self.get_register_16bit(
            self.__VL6180X_SYSALS_INTEGRATION_PERIOD)

        als_integration_period = 100.0 / als_integration_period_raw

        # Calculate actual LUX from application note
        als_calculated = \
            0.32 * (als_raw / als_gain_actual) * als_integration_period

        return als_calculated

    def get_register(self, register_address):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0])
        data = self.i2c.read_byte(self.address)
        return data

    def get_register_16bit(self, register_address):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0])
        data0 = self.i2c.read_byte(self.address)
        data1 = self.i2c.read_byte(self.address)
        return (data0 << 8) | (data1 & 0xFF)

    def set_register(self, register_address, data):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0, (data & 0xFF)])

    def set_register_16bit(self, register_address, data):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        d1 = (data >> 8) & 0xFF
        d0 = data & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0, d1, d0])
