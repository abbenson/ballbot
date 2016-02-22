import DMCC
import time

print "Cape 0; Motor 1"
DMCC.setMotor(0, 1, 5000)
time.sleep(2)
DMCC.setMotor(0, 1, 0)

print "Cape 0; Motor 2"
DMCC.setMotor(0, 2, 5000)
time.sleep(2)
DMCC.setMotor(0, 2, 0)

print "Cape 1; Motor 1"
DMCC.setMotor(1, 1, 5000)
time.sleep(2)
DMCC.setMotor(1, 1, 0)

print "Cape 1; Motor 2"
DMCC.setMotor(1, 2, 5000)
time.sleep(2)
DMCC.setMotor(1, 2, 0)
