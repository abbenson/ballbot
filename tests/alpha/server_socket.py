import socket
import pyDMCC

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ss.bind(("192.168.4.1", 9999))
print "start"
ss.listen(5)
print "client conn"

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

# Motor Direction Corrections
cape0mtr1 = 1
cape0mtr2 = 1
cape1mtr1 = -1
cape1mtr2 = -1

(cs, address) = ss.accept()
print "conn accept"
count = 0
mult = 5
min = 180
max = 375
vel = 0
while 1:
    data = cs.recv(5).decode()
    # print data

    if data[4] == "1":
        count += 1
    else:
        count = 0

    vel = min + count * mult
    if vel < min:
        vel = min
    elif vel > max:
        vel = max


    if data[0] == "1":
        pitch_motor_left.velocity = int(vel) * cape0mtr1
        pitch_motor_right.velocity = int(vel) * cape1mtr1
    elif data[3] == "1":
        pitch_motor_left.velocity = int(-1 * vel) * cape0mtr1
        pitch_motor_right.velocity = int(-1 * vel) * cape1mtr1
    else:
        pitch_motor_left.velocity = 0 * cape0mtr1
        pitch_motor_right.velocity = 0 * cape1mtr1

    if data[1] == "1":
        roll_motor_left.velocity = int(vel) * cape0mtr2
        roll_motor_right.velocity = int(vel) * cape1mtr2
    elif data[2] == "1":
        roll_motor_left.velocity = int(-1 * vel) * cape0mtr2
        roll_motor_right.velocity = int(-1 * vel) * cape1mtr2
    else:
        roll_motor_left.velocity = 0 * cape0mtr2
        roll_motor_right.velocity = 0 * cape1mtr2
