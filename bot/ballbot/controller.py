from PID import PID


class Controller:
    def __init__(self):
        self.pitch_pid = PID(25, 15, 2)
        self.roll_pid = PID(25, 15, 2)
        self.pitch = 0
        self.roll = 0
        self.pitch_pid.SetPoint = 0
        self.roll_pid.SetPoint = 0
        self.pitch_pid.sample_time = 0.00
        self.roll_pid.sample_time = 0.00
        self.pitch_pid.windup_guard = 200
        self.roll_pid.windup_guard = 200

    def update(self, pitch_new, roll_new):
        self.pitch_pid.update(pitch_new)
        self.roll_pid.update(roll_new)
