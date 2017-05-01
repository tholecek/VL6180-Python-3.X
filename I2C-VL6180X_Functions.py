import RPi.GPIO as GPIO
import time
from ST_VL6180X import VL6180X

class TASKS:
    #Constants
	i2c_default = 0x29
	
	#Ports and Pins
	#This needs to be replaced with a dynamically created set of variables,
	#For now these are the constants based on my particalur setup
	#Ports and Pins
	# .i2c is new address
	# .standby is GPIO pin number for standby state
	# . intrpt is GPIO pin number for interupt state
	#Note these are NOT Broadcom pin numbers!
	
	sensor0_i2c = 0x28
	sensor0_standby = 11
	sensor0_intrpt = 12

	sensor1_i2c = 0x29
	sensor1_standby = 13
	sensor1_intrpt = 16

	sensor2_i2c = 0x30
	sensor2_standby = 15
	sensor2_intrpt = 18

	def renumber(self)
		
