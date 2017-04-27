# Sample program to read information off ST VL6180X such as identification
# and I2C Address.  Will add function to change I2C address.


from ST_VL6180X import VL6180X

# Initialize VL6180X, hereby known as sensor
# Default I2C address is always 0x29 at power on.  This will need to be changed
# if using multiple sensors
old = 0x30
new = 0x31

sensor_i2cid = old
sensor = VL6180X(sensor_i2cid)
sensor.change_address(old,new)
