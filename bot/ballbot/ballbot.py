import re
import time
import pyDMCC
import Adafruit_BBIO.UART as UART
import serial
from controller import Controller

UART.setup("UART1")

# Motor Direction Corrections
cape0mtr1 = 1
cape0mtr2 = 1
cape1mtr1 = -1
cape1mtr2 = -1

# Setup serial connection to IMU
ser = serial.Serial(port="/dev/ttyO1", baudrate=57600)

# Initialize Controller
bot_controller = Controller()

# Initialize Velocity PIDs
dmccs = pyDMCC.autodetect()
pitch_motor_left = dmccs[0].motors[1]
pitch_motor_right = dmccs[1].motors[1]
roll_motor_left = dmccs[0].motors[2]
roll_motor_right = dmccs[1].motors[2]

constants = (-3000, -32768, 0)
pitch_motor_left.velocity_pid = constants
pitch_motor_right.velocity_pid = constants
roll_motor_left.velocity_pid = constants
roll_motor_right.velocity_pid = constants

print "starting loop"

while 1:
    try:
        # Open serial
        ser.open()
        # Take line of readings from IMU
        ser_str = ser.readline()
        while ser_str[0] != '#':
            ser_str = ser.readline()

        # Parse out float YPR values
        ser_str = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", ser_str)
        pitch_new = float(ser_str[1])
        roll_new = float(ser_str[2])
        ser.close()

        # Update PID
        bot_controller.update(0, 0, pitch_new, roll_new)
        pitch_corr = int(bot_controller.pitch_pid.output)
        roll_corr = int(bot_controller.roll_pid.output)

        # if (time.time()*1000 - last_mot_time) >= 250:
        # Set motor velocities
        print "p: %d" % pitch_corr
        print "r: %d" % roll_corr
        pitch_motor_left.velocity = pitch_corr * cape0mtr1
        pitch_motor_right.velocity = pitch_corr * cape1mtr1
        roll_motor_left.velocity = roll_corr * cape0mtr2
        roll_motor_right.velocity = roll_corr * cape1mtr2

    except KeyboardInterrupt:
        pitch_motor_left.velocity = 0
        pitch_motor_right.velocity = 0
        roll_motor_left.velocity = 0
        roll_motor_right.velocity = 0
        ser.close();
        print"closing"
        exit()