class PID:
    def __init__(self, kp, ki, kd):
        self.p_value = kp
        self.i_value = ki
        self.d_value = kd
        self.error = 0.0
        self.total_error = 0.0
        self.prev_error = 0.0
        self.set_point = 0.0
        self.max_output = 1.0
        self.min_output = -1.0

    def update_pid(self, value):
        self.error = self.set_point - value

        # Accumulate integral only if error is small to prevent "windup"
        if abs(self.error) < 500:
            self.total_error += self.error
            # Clamp integral sum to prevent runaway
            self.total_error = max(-1000, min(self.total_error, 1000))

        self.result = (self.p_value * self.error) + \
                      (self.i_value * self.total_error) + \
                      (self.d_value * (self.error - self.prev_error))
        
        self.prev_error = self.error
        return self.clamp(self.result)

    def set_set_point(self, target):
        self.set_point = target
        self.total_error = 0

    def clamp(self, val):
        return max(self.min_output, min(val, self.max_output))