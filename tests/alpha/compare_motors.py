import DMCC
import bbio
import pyDMCC
import time

tp = bbio.GPIO1_16
bbio.pinMode(tp, bbio.OUTPUT)


def motor_ex():
    DMCC.setPIDConstants(0, 2, 1, -3000, -32768, 0)

    while 1:
        try:
            bbio.digitalWrite(tp, bbio.HIGH)
            DMCC.setTargetVel(0, 2, 150)
            bbio.digitalWrite(tp, bbio.LOW)

        except KeyboardInterrupt:
            DMCC.setTargetVel(0, 2, 0)
            exit()


def motor_club():
    dmccs = pyDMCC.autodetect()
    motor = dmccs[0].motors[1]
    constants = (-15000, -30000, 0)
    motor.velocity_pid = constants
    velocity = 0

    while 1:
        try:
            bbio.digitalWrite(tp, bbio.HIGH)
            if velocity == 0:
                velocity = 450
            else:
                velocity -= 50
            motor.velocity = velocity
            time.sleep(.3)
            bbio.digitalWrite(tp, bbio.LOW)

        except KeyboardInterrupt:
            motor.velocity = 0
            exit()

motor_club()
