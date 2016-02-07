from PID import PID

class Controller:
    def __init__(self):
        self.vx_pid = PID(1, 0, 0)
        self.vy_pid = PID(1, 0, 0)
        self.pitch_pid = PID(1, 0, 0)
        self.roll_pid = PID(1, 0, 0)
        self.pitch = 0
        self.roll = 0
        self.vx = 0
        self.vy = 0
        self.vx_pid.SetPoint(0)
        self.vy_pid.SetPoint(0)
        self.pitch_pid.SetPoint(0)
        self.roll_pid.SetPoint(0)

    def update(self, vx_new, vy_new, pitch_new, roll_new):
        self.vx_pid.update(vx_new)
        self.vy_pid.update(vy_new)
        self.pitch_pid(pitch_new)
        self.roll_pid(roll_new)
