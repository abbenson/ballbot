import re
import struct
import time
import math
import pyDMCC
import Adafruit_BBIO.UART as UART
import serial
from controller import Controller


def get_velocities(pitch_vel_l, pitch_vel_r, roll_vel_l, roll_vel_r, pitch, roll):
    v_x = .5 * (pitch_vel_l + pitch_vel_r)
    v_y = .5 * (roll_vel_l + roll_vel_r)
    pitch = math.radians(pitch)
    roll = math.radians(roll)
    v_x *= math.cos(pitch)
    v_y *= math.cos(roll)
    return v_x, v_y


# @profile
def balance():
    UART.setup("UART4")

    # Motor Direction Corrections
    cape0mtr1 = 1
    cape0mtr2 = 1
    cape1mtr1 = -1
    cape1mtr2 = -1

    # Motor boundaries
    motor_max = 375
    motor_min = 0

    # Setup serial connection to IMU
    ser = serial.Serial(port="/dev/ttyO4", baudrate=57600, timeout=None)
    ser.write("#o1#ob#oe0")

    # Initialize Controller
    bot_controller = Controller()
    bot_controller.change_mode('velocity')

    # Initialize DMCCs
    dmccs = pyDMCC.autodetect()
    pitch_motor_left = dmccs[0].motors[1]
    pitch_motor_right = dmccs[1].motors[1]
    roll_motor_left = dmccs[0].motors[2]
    roll_motor_right = dmccs[1].motors[2]

    # Initialize velocity PIDs
    constants = (-3000, -32768, 0)
    pitch_motor_left.velocity_pid = constants
    pitch_motor_right.velocity_pid = constants
    roll_motor_left.velocity_pid = constants
    roll_motor_right.velocity_pid = constants

    # Pitch/roll update vars
    pitch_new = 0
    roll_new = 0

    # Config Start
    raw_input("Place on level surface and press enter to configure")

    # Sync to serial
    ser.flushInput()
    ser.write("#s00")
    while ser.inWaiting() < 15:
        pass
    ser.readline()

    # Configure angle set-point
    for i in range(0, 99, 1):
        while ser.inWaiting() < 12:
            pass

        struct.unpack('<f', ser.read(4))[0]
        pitch_new += struct.unpack('<f', ser.read(4))[0]
        roll_new += struct.unpack('<f', ser.read(4))[0]

        print "p:%f, r:%f" % (pitch_new, roll_new)

    bot_controller.pitch_pid.SetPoint = pitch_new / 100
    bot_controller.roll_pid.SetPoint = roll_new / 100

    print "Calibrated: Roll->%f    Pitch->%f" % (bot_controller.roll_pid.SetPoint, bot_controller.pitch_pid.SetPoint)

    # Start Balancing Loop
    raw_input("Place level on ball and press enter to start balancing")

    print "starting loop"
    while 1:
        try:
            # Pull new Pitch/Roll values
            struct.unpack('<f', ser.read(4))[0]
            pitch_new = struct.unpack('<f', ser.read(4))[0]
            roll_new = struct.unpack('<f', ser.read(4))[0]

            # Update Velocities
            vx_new, vy_new = get_velocities(pitch_motor_left.velocity, pitch_motor_right.velocity,
                                            roll_motor_left.velocity, roll_motor_right.velocity, pitch_new, roll_new)

            # Update Controller
            bot_controller.update(vx_new, vy_new, pitch_new, roll_new)

            # Set motors
            pitch_corr = int(bot_controller.pitch_pid.output)
            if pitch_corr > motor_max:
                pitch_corr = motor_max
            elif pitch_corr < (motor_max * -1):
                pitch_corr = motor_max * -1

            roll_corr = int(bot_controller.roll_pid.output)
            if roll_corr > motor_max:
                roll_corr = motor_max
            elif roll_corr < (motor_max * -1):
                roll_corr = motor_max * -1

            print "\r Pitch Correction: %d;     Roll Correction: %d" % (pitch_corr, roll_corr),

            # Set motor velocities
            pitch_motor_left.velocity = pitch_corr * cape0mtr1
            pitch_motor_right.velocity = pitch_corr * cape1mtr1
            roll_motor_left.velocity = roll_corr * cape0mtr2
            roll_motor_right.velocity = roll_corr * cape1mtr2

        except KeyboardInterrupt:
            pitch_motor_left.velocity = 0
            pitch_motor_right.velocity = 0
            roll_motor_left.velocity = 0
            roll_motor_right.velocity = 0
            ser.close()
            print"closing"
            exit()


balance()
