import serial
import Adafruit_BBIO.UART as UART
import binascii
import struct
import time

UART.setup("UART4")

# Setup serial connection to IMU
ser = serial.Serial(port="/dev/ttyO4", baudrate=57600, timeout=None)

# Open serial
ser.write("#o1#ob")
ser.flushInput()
ser.write("#s00")

token = "#SYNCH00\r\n"

while ser.readline() != token:
    print "Token wrong"

while 1:
    while ser.inWaiting() < 12:
        pass

    yaw = struct.unpack('<f', ser.read(4))[0]
    pitch = struct.unpack('<f', ser.read(4))[0]
    roll = struct.unpack('<f', ser.read(4))[0]

    print "y:%f, p:%f, r:%f" % (yaw, pitch, roll)
