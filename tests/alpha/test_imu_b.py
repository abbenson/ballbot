import serial
import Adafruit_BBIO.UART as UART
import binascii
import struct
import time
from bbio import *

UART.setup("UART4")

# Setup serial connection to IMU
ser = serial.Serial(port="/dev/ttyO4", baudrate=57600, timeout=None)

tp = GPIO1_16
pinMode(tp, OUTPUT)

# Open serial
ser.write("#o1#ob")
ser.flushInput()
ser.write("#s00")

print ser.readline()
ser.flushInput()

while 1:
    digitalWrite(tp, HIGH)

    y = struct.unpack('<f', ser.read(4))[0]
    p = struct.unpack('<f', ser.read(4))[0]
    r = struct.unpack('<f', ser.read(4))[0]
    digitalWrite(tp, LOW)
    print "y:%f, p:%f, r:%f" % (y, p, r)
