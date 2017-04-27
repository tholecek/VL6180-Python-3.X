# Quick and Dirty Sensor Read for multiple sensors
# Assumes i2c addresses have been change prior to run

import sys, time

from ST_VL6180X import VL6180X


#Initialize and report Sensor 0
sensor0_i2cid = 0x29
sensor0 = VL6180X(sensor0_i2cid)
sensor0.get_identification()
if sensor0.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor0.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor0.idModel))
sensor0.default_settings()
#Finish Initialize Sensor 0
#---------------------------------
#Initialize and report Sensor 1
sensor1_i2cid = 0x32
sensor1 = VL6180X(sensor1_i2cid)
sensor1.get_identification()
if sensor1.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor1.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor1.idModel))
sensor1.default_settings()
#Finish Initialize Sensor 1
#---------------------------------
#Initialize and report Sensor 2
sensor2_i2cid = 0x35
sensor2 = VL6180X(sensor2_i2cid)
sensor2.get_identification()
if sensor2.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor2.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor2.idModel))
sensor2.default_settings()
#Finish Initialize Sensor 2
# Quick Test Code To read TOF sensor

for i in range(10):
    L0 = int(sensor0.get_distance())
    print("Sensor 29 reports ",L0,"mm")
    L1 = int(sensor1.get_distance())
    print("Sensor 32 reports ",L1,"mm")
    L2 = int(sensor2.get_distance())
    print("Sensor 35 reports ",L2,"mm\n")
    time.sleep(1)

#Test results show code was successful reading both sensors
#27APR17 TAH
