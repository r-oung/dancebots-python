#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .step import Step

class Light:
    """Light"""

    def __init__(self, unit="beats"):
        if unit != "beats" and unit != "seconds":
            raise ValueError("unit must either be 'beats' or 'seconds'")
        
        self._steps = []
        self._unit = unit

    def _append_step(self, num_units, leds):
        if num_units < 0:
            raise ValueError("num_units must be a positive value")

        if len(leds) != 8:
            raise ValueError("led list must contain 8 values")

        for led in leds:
            if led != 0 and led != 1:
                raise ValueError("led value must be either 0 or 1")

        self._steps.append(Step([0] * 8, [0] * 8, leds, self._unit, num_units))

    def blink(self, leds, num_units, freq=1):
        if freq < 1 or not isinstance(freq, int):
            raise ValueError("freq must be a positive integer")

        num_steps = num_units * freq
        for i in range(num_steps):
            self._append_step(1 / freq, leds)

            # Toggle LEDs
            leds = [int(not led) for led in leds]

    def hold(self, leds, num_units):
        self._append_step(num_units, leds)

    def stop(self, num_units):
        self._append_step(num_units, [0] * 8)
    
    def clear(self):
        self._steps = []

    @property
    def steps(self):
        return self._steps

    def __str__(self):
        # pretty print steps
        lines = []

        if self._unit == "beats":
            header = ["Step", "LEDs", "Beats"]
        elif self._unit == "seconds":
            header = ["Step", "LEDs", "Seconds"]

        format_row = "{:<6} {:<26} {:<7}"
        lines.append(format_row.format(*header))

        for num, step in enumerate(self._steps, start=1):
            lines.append(format_row.format(num, str(step.leds), step.num_units))

        return "\n".join(lines)
