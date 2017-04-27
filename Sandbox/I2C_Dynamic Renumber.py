#Program used to create code to change multiple I2C addresses on the VL6180X

import RPi.GPIO as GPIO
import time
from ST_VL6180X import VL6180X

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)
GPIO.output(16,True)

sensor0_i2cid = 0x32
sensor0 = VL6180X(sensor0_i2cid)
sensor0.get_identification()
if sensor0.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor0.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor0.idModel))
time.sleep(1)
print("Shutting Down")
time.sleep(5)
print("Starting Up")
time.sleep(1)
sensor0.get_identification()
if sensor0.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor0.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor0.idModel))


GPIO.cleanup()
