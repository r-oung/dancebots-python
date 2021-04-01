#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Frame:
    """Dancebots protocol frame"""

    _start_duration = 2.0  # start bit duration [msec]
    _one_duration = 0.7  # one bit duration [msec]
    _zero_duration = 0.2  # zero bit duration [msec]

    def _start(self):
        num_samples = int(self._start_duration * (self._sample_rate / 1000.0))

        for x in range(num_samples):
            self._bitstream.append(1)

    def _one(self):
        num_samples = int(self._one_duration * (self._sample_rate / 1000.0))

        for x in range(num_samples):
            self._bitstream.append(1)

    def _zero(self):
        num_samples = int(self._zero_duration * (self._sample_rate / 1000.0))

        for x in range(num_samples):
            self._bitstream.append(0)

    def _clear(self):
        self._bitstream = []

    def __init__(
        self, motor_l=[0] * 8, motor_r=[0] * 8, leds=[0] * 8, sample_rate=44100
    ):
        self._bitstream = []
        self._sample_rate = sample_rate

        if len(motor_l) != 8:
            raise ValueError("Left motor must contain at least 8 values")

        if len(motor_r) != 8:
            raise ValueError("Right motor must contain at least 8 values")

        if len(leds) != 8:
            raise ValueError("LEDs must contain at least 8 values")

        self._start()

        frame = motor_l + motor_r + leds
        for x in frame:
            if x == 1:
                self._one()
            elif x == 0:
                self._zero()
            else:
                raise ValueError("Frame must contain binary values, i.e. 0 or 1")

    @property
    def bitstream(self):
        return self._bitstream

    @property
    def length(self):
        return len(self._bitstream)

    @property
    def duration(self):
        sample_period = 1.0 / self._sample_rate
        return len(self._bitstream) * sample_period  # [seconds]

    def __str__(self):
        return str(self._bitstream)


if __name__ == "__main__":
    motor_l = [0, 1, 1, 1, 1, 0, 1, 0]
    motor_r = [0, 1, 1, 1, 1, 0, 1, 0]
    leds = [0, 1, 0, 1, 0, 1, 0, 1]
    frame = Frame(motor_l, motor_r, leds)
    print(frame)
    print("Duration: {} seconds".format(round(frame.duration, 2)))
