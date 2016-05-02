import re
import struct
import time
import math
import os
import pyDMCC
import Adafruit_BBIO.UART as UART
import serial
import csv
from controller import Controller
from bbio import *


# @profile
def balance():
    """
    The main balancing code put into a function for the purposes of analysing performance
    """
    # Increase process priority
    print os.nice(-20)

    # Setup test point
    tp = GPIO1_16
    pinMode(tp, OUTPUT)

    # Setup UART
    UART.setup("UART4")

    # Open logging csv
    f = open('test.csv', 'wb')
    wr = csv.writer(f)
    wr.writerow(('t', 'x_in', 'x_out', 'y_in', 'y_out'))

    # Motor Direction Corrections
    cape0mtr1 = 1
    cape0mtr2 = -1
    cape1mtr1 = -1
    cape1mtr2 = 1

    # Motor boundaries
    motor_max = 300
    angle_max = 15

    # Setup serial connection to IMU
    ser = serial.Serial(port="/dev/ttyO4", baudrate=57600, timeout=None)

    # Set IMU to continuous output, binary mode
    ser.write("#o1#ob")

    # Initialize DMCCs
    dmccs = pyDMCC.autodetect()
    pitch_motor_left = dmccs[0].motors[2]
    pitch_motor_right = dmccs[1].motors[2]
    roll_motor_left = dmccs[0].motors[1]
    roll_motor_right = dmccs[1].motors[1]

    # Initialize velocity PIDs
    constants = (-11500, -30000, 0)
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
    ser.write("#s02")
    print ser.readline()
    # ser.flushInput()

    pitch_config = 0
    roll_config = 0

    # Configure angle set-point
    for i in range(0, 99, 1):
        # ser.write("#f")
        while ser.inWaiting() < 12:
            pass
        ser.read(4)
        pitch_config += struct.unpack('<f', ser.read(4))[0]
        roll_config += struct.unpack('<f', ser.read(4))[0]

        print "p:%f, r:%f" % (pitch_config, roll_config)

    pitch_config /= 100
    roll_config /= 100

    # Initialize Controller
    bot_controller = Controller()
    bot_controller.pitch_pid.SetPoint = pitch_config
    bot_controller.roll_pid.SetPoint = roll_config

    print "Calibrated: Roll->%f    Pitch->%f" % (bot_controller.roll_pid.SetPoint, bot_controller.pitch_pid.SetPoint)

    # Start Balancing Loop
    raw_input("Place level on ball and press enter to start balancing")

    print "starting loop"
    time_start = time.time()

    pitch_old = 0
    roll_old = 0

    # Main loop
    while 1:
        try:
            pitch_old = pitch_new
            roll_old = roll_new

            # Pull new Pitch/Roll values
            # ser.write('#f')
            while ser.inWaiting() < 12:
                pass
            ser.read(4)
            pitch_new = struct.unpack('<f', ser.read(4))[0]
            roll_new = struct.unpack('<f', ser.read(4))[0]

            # Check for good values
            if pitch_new > 100 or pitch_new < -100 or roll_new > 100 or roll_new < -100:
                # We've likely lost sync so we need to sync again
                ser.flushInput()
                print ser.write("#s02")
                ser.readline()
                continue

            # if pitch_new*pitch_old < 0:
            #     bot_controller.pitch_pid.ITerm = 0
            # if roll_new*roll_old < 0:
            #     bot_controller.roll_pid.ITerm = 0

            # Update Controller
            bot_controller.update(pitch_new, roll_new)

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

            wr.writerow((time.time() - time_start, pitch_new, bot_controller.pitch_pid.DTerm, roll_new, roll_corr))

            digitalWrite(tp, HIGH)
            # Set motor velocities
            pitch_motor_left.velocity = pitch_corr * cape0mtr1
            pitch_motor_right.velocity = pitch_corr * cape1mtr1
            roll_motor_left.velocity = roll_corr * cape0mtr2
            roll_motor_right.velocity = roll_corr * cape1mtr2
            digitalWrite(tp, LOW)

        except KeyboardInterrupt:
            break

    pitch_motor_left.velocity = 0
    pitch_motor_right.velocity = 0
    roll_motor_left.velocity = 0
    roll_motor_right.velocity = 0
    ser.close()
    f.close()
    print "\nclosing"
    exit()

balance()
