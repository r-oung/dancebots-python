#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Frame:
    """Dancebots protocol frame"""

    _start_duration = 2.0  # start bit duration [msec]
    _one_duration = 0.7  # one bit duration [msec]
    _zero_duration = 0.2  # zero bit duration [msec]

    def __init__(self, sample_rate=44100):
        self._samples = []
        self._sample_rate = sample_rate

    def _start(self):
        num_samples = int(self._start_duration * (self._sample_rate / 1000.0))

        for x in range(num_samples):
            self._samples.append(1.0)

        return

    def _one(self):
        num_samples = int(self._one_duration * (self._sample_rate / 1000.0))

        for x in range(num_samples):
            self._samples.append(1.0)

        return

    def _zero(self):
        num_samples = int(self._zero_duration * (self._sample_rate / 1000.0))

        for x in range(num_samples):
            self._samples.append(0.0)

        return

    def create(self, l_motor=[0] * 8, r_motor=[0] * 8, leds=[0] * 8):
        if len(l_motor) != 8:
            raise ValueError("Left motor must contain at least 8 values")

        if len(r_motor) != 8:
            raise ValueError("Right motor must contain at least 8 values")

        if len(leds) != 8:
            raise ValueError("LEDs must contain at least 8 values")

        self._start()

        frame = l_motor + r_motor + leds
        for x in frame:
            if x == 1:
                self._one()
            elif x == 0:
                self._zero()
            else:
                raise ValueError("Frame must contain binary values, i.e. 0 or 1")

        return

    @property
    def bitstream(self):
        return self._samples

    @property
    def duration(self):
        sample_period = 1.0 / self._sample_rate
        return len(self._samples) * sample_period


if __name__ == "__main__":
    frame = Frame()
    l_motor = [0, 1, 1, 1, 1, 0, 1, 0]
    r_motor = [0, 1, 1, 1, 1, 0, 1, 0]
    leds = [0, 1, 0, 1, 0, 1, 0, 1]
    frame.create(l_motor, r_motor, leds)
    print(frame.bitstream)
    print(frame.duration)
