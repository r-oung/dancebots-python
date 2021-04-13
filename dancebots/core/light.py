# -*- coding: utf-8 -*-
"""Lights sequence class.

Defines a light sequence.
"""
from .step import Step


class Light:
    """Defines a light sequence.

    Attributes:
            unit: Can either be "beats" or "seconds".
    """

    def __init__(self):
        self._steps = []

    def _append_step(self, num_units, leds):
        if num_units < 0:
            raise ValueError("num_units must be a positive value")

        if len(leds) != 8:
            raise ValueError("led list must contain 8 values")

        for led in leds:
            if led not in (0, 1):
                raise ValueError("led value must be either 0 or 1")

        self._steps.append(Step([0] * 8, [0] * 8, leds, num_units))

    def blink(self, leds, num_units, freq=1):
        """Blink lights.

        Attributes:
                leds: List of bits for controlling the lights.
                freq: Blink/toggling frequency (per unit)
        """
        if num_units < 1 or not isinstance(num_units, int):
            raise ValueError("num_units must be a positive integer")

        if freq < 1 or not isinstance(freq, int):
            raise ValueError("freq must be a positive integer")

        num_steps = num_units * freq
        for _ in range(num_steps):
            self._append_step(1 / freq, leds)

            # Toggle LEDs
            leds = [int(not led) for led in leds]

    def hold(self, leds, num_units):
        """Hold lights.

        Attributes:
                leds: List of bits for controlling the lights.
                num_units: The number of units to keep the lights on and/or off.
        """
        self._append_step(num_units, leds)

    def stop(self, num_units):
        """Turn off all lights.

        Attributes:
                num_units: The number of units to keep the lights off.
        """
        self._append_step(num_units, [0] * 8)

    def clear(self):
        """Clear steps.

        Clears the lights sequence.
        """
        self._steps = []

    @property
    def steps(self):
        """List of light sequence steps"""
        return self._steps

    def __str__(self):
        """Pretty print steps"""
        lines = []

        header = ["Step", "LEDs", "Beats"]
        format_row = "{:<6} {:<26} {:<7}"
        lines.append(format_row.format(*header))

        for num, step in enumerate(self._steps, start=1):
            lines.append(format_row.format(num, str(step.leds), step.num_units))

        return "\n".join(lines)
