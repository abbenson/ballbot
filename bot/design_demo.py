import Adafruit_BBIO.UART as UART
import serial
import re
import pyDMCC

# Autodetect DMCC capes
dmccs = pyDMCC.autodetect()

pitch_power = 0
roll_power = 0

UART.setup("UART1")

# Open serial connection to IMU
ser = serial.Serial(port="/dev/ttyO1", baudrate=57600)

# Demo loop
while 1:
    ser.open()

    # Take line of readings from IMU
    ser_str = ser.readline()
    while ser_str[0] != '#':
        ser_str = ser.readline()

    # Parse out float YPR values
    ser_str = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", ser_str)

    # Set Pitch Motor
    # If pitch between -10 and 10 set motor off
    if -10 < float(ser_str[1]) < 10:
        if pitch_power != 0:
            print "Pitch Motor Off"
            pitch_power = 0
            dmccs[0].motors[1].power = pitch_power

    # If pitch between 10 and 20 set motor 35%
    elif 10 <= float(ser_str[1]) < 20:
        if pitch_power != 35:
            print "Pitch Motor Forward 35%"
            pitch_power = 35
            dmccs[0].motors[1].power = pitch_power

    # If pitch between 20 and 30 set motor 50%
    elif 20 <= float(ser_str[1]) < 30:
        if pitch_power != 50:
            print "Pitch Motor Forward 50%"
            pitch_power = 50
            dmccs[0].motors[1].power = pitch_power

    # If pitch between 30 and 40 set motor 75%
    elif 30 <= float(ser_str[1]) < 40:
        if pitch_power != 75:
            print "Pitch Motor Forward 75%"
            pitch_power = 75
            dmccs[0].motors[1].power = pitch_power

    # If pitch greater than 40 set motor 100%
    elif float(ser_str[1]) >= 40:
        if pitch_power != 100:
            print "Pitch Motor Forward 100%"
            pitch_power = 100
            dmccs[0].motors[1].power = pitch_power

    # If pitch between -10 and -20 set motor -35%
    elif -20 < float(ser_str[1]) <= -10:
        if pitch_power != -35:
            print "Pitch Motor Reverse 35%"
            pitch_power = -35
            dmccs[0].motors[1].power = pitch_power

    # If pitch between -20 and -30 set motor -50%
    elif -30 < float(ser_str[1]) <= -20:
        if pitch_power != -50:
            print "Pitch Motor Reverse 50%"
            pitch_power = -50
            dmccs[0].motors[1].power = pitch_power

    # If pitch between -30 and -40 set motor -75%
    elif -40 < float(ser_str[1]) <= -30:
        if pitch_power != -75:
            print "Pitch Motor Reverse 75%"
            pitch_power = -75
            dmccs[0].motors[1].power = pitch_power

    # If pitch less than -40 set motor -100%
    elif float(ser_str[1]) <= -40:
        if pitch_power != -100:
            print "Pitch Motor Reverse 100%"
            pitch_power = -100
            dmccs[0].motors[1].power = pitch_power

    # Set Roll Motor
    # If roll between -10 and 10 set motor off
    if -10 < float(ser_str[2]) < 10:
        if roll_power != 0:
            print "Roll Motor Off"
            roll_power = 0
            dmccs[0].motors[2].power = roll_power

    # If roll between 10 and 20 set motor 35%
    elif 10 <= float(ser_str[2]) < 20:
        if roll_power != 35:
            print "Roll Motor Forward 35%"
            roll_power = 35
            dmccs[0].motors[2].power = roll_power

    # If roll between 20 and 30 set motor 50%
    elif 20 <= float(ser_str[2]) < 30:
        if roll_power != 50:
            print "Roll Motor Forward 50%"
            roll_power = 50
            dmccs[0].motors[2].power = roll_power

    # If roll between 30 and 40 set motor 75%
    elif 30 <= float(ser_str[2]) < 40:
        if roll_power != 75:
            print "Roll Motor Forward 75%"
            roll_power = 75
            dmccs[0].motors[2].power = roll_power

    # If roll greater than 40 set motor 100%
    elif float(ser_str[2]) >= 40:
        if roll_power != 100:
            print "Roll Motor Forward 100%"
            roll_power = 100
            dmccs[0].motors[2].power = roll_power

    # If roll between -10 and -20 set motor -35%
    elif -20 < float(ser_str[2]) <= -10:
        if roll_power != -35:
            print "Roll Motor Reverse 35%"
            roll_power = -35
            dmccs[0].motors[2].power = roll_power

    # If roll between -20 and -30 set motor -50%
    elif -30 < float(ser_str[2]) <= -20:
        if roll_power != -50:
            print "Roll Motor Reverse 50%"
            roll_power = -50
            dmccs[0].motors[2].power = roll_power

    # If roll between -30 and -40 set motor -75%
    elif -40 < float(ser_str[2]) <= -30:
        if roll_power != -75:
            print "Roll Motor Reverse 75%"
            roll_power = -75
            dmccs[0].motors[2].power = roll_power

    # If roll less than -40 set motor -100%
    elif float(ser_str[2]) <= -40:
        if roll_power != -100:
            print "Roll Motor Reverse 100%"
            roll_power = -100
            dmccs[0].motors[2].power = roll_power

    ser.close()
