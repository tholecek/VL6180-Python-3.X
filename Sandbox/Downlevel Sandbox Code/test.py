import RPi.GPIO as GPIO
import time
from ST_VL6180X import VL6180X
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
time.sleep(0.05)
GPIO.output(11,True)
GPIO.output(13,True)
GPIO.output(15,True)
time.sleep(4)
GPIO.output(11,False)
GPIO.output(13,False)
GPIO.output(15,False)
time.sleep(10)
###Exit Program
GPIO.output(11,True)
GPIO.output(13,True)
GPIO.output(15,True)
time.sleep(4)
GPIO.cleanup()
