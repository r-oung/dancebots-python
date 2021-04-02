#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Frame:
    """Dancebots protocol frame"""

    # Static variables
    _START = 2.0  # start bit duration [msec]
    _ONE = 0.7  # one bit duration [msec]
    _ZERO = 0.2  # zero bit duration [msec]

    def __init__(self, motor_l=[0] * 8, motor_r=[0] * 8, leds=[0] * 8, sample_rate=44100):
        # Non-static variables
        self._sample_rate = sample_rate
        self._last_value = 1  # WAV value; toggles between -1 and +1
        self._data = [] # list of bits

        if len(motor_l) != 8:
            raise ValueError("Left motor must contain at least 8 values")

        if len(motor_r) != 8:
            raise ValueError("Right motor must contain at least 8 values")

        if len(leds) != 8:
            raise ValueError("LEDs must contain at least 8 values")

        self._append(self._START)

        frame = motor_l + motor_r + leds
        for x in frame:
            if x == 1:
                self._append(self._ONE)
            elif x == 0:
                self._append(self._ZERO)
            else:
                raise ValueError("Frame must contain binary values, i.e. 0 or 1")

    def _append(self, duration):
        self._last_value *= -1  # toggle value
        num_samples = int(duration * (self._sample_rate / 1000.0))
        for x in range(num_samples):
            self._data.append(self._last_value)

    @property
    def data(self):
        return self._data

    @property
    def length(self):
        return len(self._data)

    @property
    def duration(self):
        sample_period = 1.0 / self._sample_rate
        return len(self._data) * sample_period  # [seconds]

    def __str__(self):
        return str(self._data)

    def __add__(self, other):
        if self._sample_rate != other._sample_rate:
            raise ValueError("Sampling rates are different")

        # Make a copy of this instance
        frame = Frame(self._sample_rate)
        frame._last_value = other._last_value

        # If last bit of this frame is the same as the first 
        # bit of the other frame, then flip the bits in the other frame
        # Note: First bit of a frame is always -1
        if self._last_value == -1:
            frame._data = self.data + [x*-1 for x  in other.data]
        else:
            frame._data = self.data + other.data
        
        return frame

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

if __name__ == "__main__":
    motor_l = [0, 1, 1, 1, 1, 0, 1, 0]
    motor_r = [0, 1, 1, 1, 1, 0, 1, 0]
    leds = [0, 1, 0, 1, 0, 1, 0, 1]
    frame = Frame(motor_l, motor_r, leds)
    print(frame)
    print("Duration: {:.4} seconds".format(frame.duration))
