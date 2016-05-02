import pyDMCC
import time
from Adafruit_I2C import Adafruit_I2C

# Motor Direction Corrections
cape0mtr1 = 1
cape0mtr2 = -1
cape1mtr1 = -1
cape1mtr2 = 1

# Initialize DMCCs
dmccs = pyDMCC.autodetect()
pitch_motor_left = dmccs[0].motors[2]
pitch_motor_right = dmccs[1].motors[2]
roll_motor_left = dmccs[0].motors[1]
roll_motor_right = dmccs[1].motors[1]

# Initialize velocity PIDs
constants = (-3000, -32768, 0)
pitch_motor_left.velocity_pid = constants
pitch_motor_right.velocity_pid = constants
roll_motor_left.velocity_pid = constants
roll_motor_right.velocity_pid = constants

cape1 = Adafruit_I2C(0x2c)
cape2 = Adafruit_I2C(0x2d)

print "writing"
pitch_motor_left.velocity = -10
print "written"
