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
        self.vx_pid.SetPoint = 0
        self.vy_pid.SetPoint = 0
        self.pitch_pid.SetPoint = 0
        self.roll_pid.SetPoint = 0
        self.pitch_pid.sample_time = 0.00
        self.roll_pid.sample_time = 0.00
        self.mode = 'pitch'

    def update(self, vx_new, vy_new, pitch_new, roll_new):
        if self.mode == 'pitch':
            self.pitch_pid.update(pitch_new)
            self.roll_pid.update(roll_new)
        elif self.mode == 'velocity':
            self.vx_pid.update(vx_new)
            self.vy_pid.update(vy_new)
            self.pitch_pid.SetPoint = self.vx_pid.output
            self.roll_pid.SetPoint = self.vy_pid.output
            self.pitch_pid.update(pitch_new)
            self.roll_pid.update(roll_new)

    def change_mode(self, new_mode):
        assert isinstance(new_mode, object)
        self.mode = new_mode
