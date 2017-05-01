# Quick and Dirty Sensor Read for multiple sensors
# Assumes i2c addresses have been change prior to run

import sys, time
import i2c_Renumber
from ST_VL6180X import VL6180X
import tkinter as tk


#Initialize and report Sensor 0
sensor0_i2cid = 0x28
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
sensor1_i2cid = 0x29
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
sensor2_i2cid = 0x30
sensor2 = VL6180X(sensor2_i2cid)
sensor2.get_identification()
if sensor2.idModel != 0xB4:
    print("Not Valid Sensor, Id reported as ",hex(sensor2.idModel))
else:
    print("Valid Sensor, ID reported as ",hex(sensor2.idModel))
sensor2.default_settings()
#Finish Initialize Sensor 2
# Quick Test Code To read TOF sensor
##for i in range(0,20):
##    L0 = int(sensor0.get_distance())
##    time.sleep(0.002)
##    L1 = int(sensor1.get_distance())
##    time.sleep(0.002)
##    L2 = int(sensor2.get_distance())
##    time.sleep(0.002)
##    print("     ",L1,"mm\n")
##    print(L0,"mm       ",L2,"mm\n\n\n")
##    time.sleep(0.1)
##    
##
###Test results show code was successful reading both sensors
###27APR17 TAH


position = 0 
def position_label(label):
  def count():
    global counter

    L0 = int(sensor0.get_distance())
    time.sleep(0.002)
    L1 = int(sensor1.get_distance())
    time.sleep(0.002)
    L2 = int(sensor2.get_distance())
    time.sleep(0.002)  
    label.config(text=L0)
    time.sleep(0.01)
  count()
 
 
root = tk.Tk()
root.title("Reading Sensors")
label = tk.Label(root, fg="green")
label.pack()
position_label(label)
button = tk.Button(root, text='Stop', width=25, command=root.destroy)
button.pack()
root.mainloop()

