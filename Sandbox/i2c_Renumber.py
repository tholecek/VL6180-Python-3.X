#Program used to create code to change multiple I2C addresses on the VL6180X

import RPi.GPIO as GPIO
import time
from ST_VL6180X import VL6180X

#Constants
i2c_default = 0x29

#Ports and Pins
sensor0_i2c = 0x28
sensor0_standby = 11
sensor0_intrpt = 12

sensor1_i2c = 0x29
sensor1_standby = 13
sensor1_intrpt = 16

sensor2_i2c = 0x30
sensor2_standby = 15
sensor2_intrpt = 18

pinouts = [sensor0_standby,sensor0_intrpt, \
           sensor1_standby,sensor1_intrpt, \
           sensor2_standby,sensor2_intrpt]

i2caddress = [sensor0_i2c,sensor1_i2c,sensor2_i2c]


#Configure GPIO Bus and Set Lines High
GPIO.setmode(GPIO.BOARD)
for i in pinouts:
    GPIO.setup(i,GPIO.OUT)
    GPIO.output(i,True)
#Wait 20 mSec between configs
    time.sleep(0.02)

time.sleep(0.1)
#Renumber I2C Addresses
##
#Sensor 0
#Put Sensor 1 and 2 into standby
GPIO.output(13,False)
GPIO.output(15,False)
time.sleep(0.100)
#Configure and Change Address
#Error Handler in Event that no Default I2c Addresses are present
try:
    sensor0 = VL6180X(i2c_default)
except IOError:
    print("No I2C Device with that address is present")
else:
    sensor0.change_address(i2c_default,sensor0_i2c)
    sensor0.default_settings()
    print("sensor 0 is at address ",hex(sensor0_i2c))
    time.sleep(0.100)
#Take Sensor 1 and 2 out of Standby
GPIO.output(13,True)
GPIO.output(15,True)
time.sleep(0.100)
####
####
###Sensor 1
###Put Sensor 0 and 2 into standby
###GPIO.output(15,False)
##time.sleep(0.100)
###Configure and Change Address
###Error Handler in Event that no Default I2c Addresses are present
###try:
##sensor1 = VL6180X(i2c_default)
###except IOError:
###print("No I2C Device with that address is present")
###else:
##sensor1.change_address(i2c_default,sensor1_i2c)
##sensor1.default_settings()
##print("sensor 1 is at address ",hex(sensor1_i2c))
##time.sleep(0.100)
###Take Sensor 0 and 2 out of Standby
##GPIO.output(11,True)
##GPIO.output(15,True)
##time.sleep(0.100)


##
##
#Sensor 2
#Put Sensor 0 and 1 into standby
GPIO.output(11,False)
GPIO.output(13,False)
time.sleep(0.100)
#Configure and Change Address
#Error Handler in Event that no Default I2c Addresses are present
try:
    sensor2 = VL6180X(i2c_default)
except IOError:
    print("No I2C Device with that address is present")
else:
    sensor2.change_address(i2c_default,sensor2_i2c)
    print("sensor 2 is at address ",hex(sensor2_i2c))
    time.sleep(0.100)
#Take Sensor 0 and 1 out of Standby
GPIO.output(11,True)
GPIO.output(13,True)
time.sleep(0.100)


###Exit Program

GPIO.cleanup()
