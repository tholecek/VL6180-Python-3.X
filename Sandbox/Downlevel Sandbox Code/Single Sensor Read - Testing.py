#Simple VL6180X Demo To Test Capabilities of Functions

import RPi.GPIO as GPIO
import time
from ST_VL6180X import VL6180X

#Set i2c address 
sensor_i2cid = 0x29

#Set GPIO line location 
sensor_gpio0 = 11
sensor_gpio1 =12

#Initial GPIO Lines
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_gpio0,GPIO.OUT)
GPIO.setup(sensor_gpio1,GPIO.OUT)

#Turn GPIO Lines On For Chip Power On
GPIO.output(sensor_gpio0,True)
GPIO.output(sensor_gpio1,True)

#Initialize VL6180X
sensor = VL6180X(sensor_i2cid)
time.sleep(0.1)

#Verify Chip ID (Optional)
sensor.get_identification()
if sensor.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor.idModel))
time.sleep(0.25)

#Main Program For Test
GPIO.output(sensor_gpio1,False)
time.sleep(5)
ToFrange = int(sensor.get_distance())
print("Sensor reports ",ToFrange,"mm")
time.sleep(0.1)
GPIO.output(sensor_gpio1,True)

#Exit Cleanup
GPIO.cleanup()
