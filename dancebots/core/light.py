#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Light:
    """Light"""

    def __init__(self):
        self._steps = []

    def _append_step(self, beats, leds):
        if len(leds) != 8:
            raise ValueError("LED list must be of length 8")

        for led in leds:
            if led != 0 and led != 1:
                raise ValueError("LED value must be either 0 or 1")

        if beats < 0:
            raise ValueError("Beats must be a positive value")

        self._steps.append(
            {
                "beats": beats,
                "leds": leds,
            }
        )

    def blink(self, leds, beats, freq=1):
        if not isinstance(freq, int) or freq < 1:
            raise ValueError("Frequency must be a positive integer")

        num_steps = beats * freq
        for i in range(num_steps):
            self._append_step(1 / freq, leds)

            # Toggle LEDs
            leds = [int(not led) for led in leds]

    def hold(self, leds, beats):
        self._append_step(beats, leds)

    def stop(self, beats):
        self._append_step(beats, [0] * 8)

    @property
    def steps(self):
        return self._steps

    def __str__(self):
        summary = "\n"

        header = ["Step", "LEDs", "Beats"]
        format_row = "{:<6} {:<26} {:<7}"
        summary += format_row.format(*header)
        summary += "\n"

        for num, step in enumerate(self._steps, start=1):
            summary += format_row.format(num, str(step["leds"]), step["beats"])
            summary += "\n"

        return summary


if __name__ == "__main__":
    leds = Light()
    leds.blink([0, 1, 0, 1, 0, 1, 0, 1], 2, 4)
    leds.blink([1, 0, 1, 0, 1, 0, 1, 0], 2, 2)
    leds.hold([1] * 8, 4)
    leds.stop(1)
    print(leds)
