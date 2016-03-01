import re
import time
import math
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

motor_forward_max = 375
motor_forward_min = 180
motor_reverse_max = -375
motor_reverse_min = -180

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

motor_time = 0
pitch_left_vel = 0
pitch_right_vel = 0
roll_left_vel = 0
roll_right_vel = 0
R = 1

print "starting loop"


def get_velocities(p_l, p_r, r_l, r_r):
    v_x = .5 * (p_l + p_r)
    v_y = .5 * (r_l + r_r)
    w_x = v_x / R
    w_y = v_y / R
    v_x *= math.cos(w_x)
    v_y *= math.cos(w_y)
    return v_x, v_y


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

        # Update Relative Velocities
        v_x_new, v_y_new = get_velocities(pitch_motor_left.velocity, pitch_motor_right.velocity,
                                          roll_motor_left.velocity,
                                          roll_motor_right.velocity)

        # Update PID
        bot_controller.update(v_x_new, v_y_new, pitch_new, roll_new)

        pitch_corr = int(bot_controller.pitch_pid.output)
        if pitch_corr > motor_forward_max:
            pitch_corr = motor_forward_max
        elif pitch_corr < motor_reverse_max:
            pitch_corr = motor_reverse_max

        roll_corr = int(bot_controller.roll_pid.output)
        if roll_corr > motor_forward_max:
            roll_corr = motor_forward_max
        elif roll_corr < motor_reverse_max:
            roll_corr = motor_reverse_max

        print "\r Pitch Correction: %d;     Roll Correction: %d" % (pitch_corr, roll_corr),

        # if (time.time()*1000 - motor_time) >= 750:
        # Set motor velocities
        # print "motor set"
        pitch_motor_left.velocity = pitch_corr * cape0mtr1
        pitch_motor_right.velocity = pitch_corr * cape1mtr1
        roll_motor_left.velocity = roll_corr * cape0mtr2
        roll_motor_right.velocity = roll_corr * cape1mtr2

        motor_time = time.time() * 1000

    except KeyboardInterrupt:
        pitch_motor_left.velocity = 0
        pitch_motor_right.velocity = 0
        roll_motor_left.velocity = 0
        roll_motor_right.velocity = 0
        ser.close()
        print"closing"
        exit()
