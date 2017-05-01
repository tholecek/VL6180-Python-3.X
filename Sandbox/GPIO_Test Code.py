#General Test Code to Turn on/off GPIO Ports


import RPi.GPIO as GPIO
import time

# Pin Number 11 is GPIO 0 (Broadcom 17)
#PinNum = 11
# Pin Number 12 is GPIO 1  (Broadcom 18)
#PinNum = 12
# Pin Number 13 is GPIO 2
#PinNum = 13
# Pin Number 15 is GPIO 3
PinNum = 15
# Pin Number 16 is GPIO 4
#PinNum = 16
# Pin Number 18 is GPIO 5
#PinNum = 18
# Pin Number 22 is GPIO 6
#PinNum = 22
# Pin Number 7 is GPIO 7
#PinNum = 7
#GPIO 8 and 9 Should Not Be Used with I2C
# Pin Number 24 is GPIO 10
#PinNum = 24
# Pin Number 26 is GPIO 11
#PinNum = 26
# Pin Number 19 is GPIO 12
#PinNum = 19


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.output(11,False)
GPIO.output(16,False)
GPIO.setup(PinNum,GPIO.OUT)
print("port Line Low")
GPIO.output(PinNum,False)
time.sleep(6)
print("Port Line High")
GPIO.output(PinNum,True)
time.sleep(6)
print("port Line Low")
GPIO.output(PinNum,False)
time.sleep(2)
print("Finished")
GPIO.output(PinNum,True)
time.sleep(1)
GPIO.cleanup()
