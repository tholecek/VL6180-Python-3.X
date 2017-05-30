#Program used to create code to change multiple I2C addresses on the VL6180X

import RPi.GPIO as GPIO
import time
from ST_VL6180X import VL6180X

#Constants
i2c_default = 0x29

#Ports and Pins

sensorcount = 3
i2caddress = [0x28,0x29,0x30];
standbypin = [11,13,15];
intrptpin = [12,16,18];

count = 0

while (sensorcount > 0):
    if (count == 0):
        sensor0_i2c = i2caddress[count]
        sensor0_standby = standbypin[count]
        sensor0_intrpt = intrptpin[count]
        
    elif (count == 1):
        sensor1_i2c = i2caddress[count]
        sensor1_standby = standbypin[count]
        sensor1_intrpt = intrptpin[count]

    elif (count == 2):
        sensor2_i2c = i2caddress[count]
        sensor2_standby = standbypin[count]
        sensor2_intrpt = intrptpin[count]

    else:
        print("Allowable number of Sensors Exceeded")

    count += 1
    sensorcount -=1

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


#Sensor 1
#Put Sensor 0 and 2 into standby
GPIO.output(15,False)
time.sleep(0.100)
#Configure and Change Address
#Error Handler in Event that no Default I2c Addresses are present
try:
    sensor1 = VL6180X(i2c_default)
except IOError:
    print("No I2C Device with that address is present")
else:
    sensor1.change_address(i2c_default,sensor1_i2c)
    sensor1.default_settings()
    print("sensor 1 is at address ",hex(sensor1_i2c))
time.sleep(0.100)
#Take Sensor 0 and 2 out of Standby
GPIO.output(11,True)
GPIO.output(15,True)
time.sleep(0.100)
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
