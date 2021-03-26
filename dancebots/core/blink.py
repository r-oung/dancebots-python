#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Blink:
    """Blink"""

    def __init__(self, max_freq=4):
        self._max_freq = max_freq
        self._steps = []

    def _append_step(self, beats, leds):
        if len(leds) != 8:
            raise ValueError("LED list must be of length 8")
        
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
        for i in range(1, num_steps):
            self._append_step(1 / freq, leds)
            
            # Toggle LEDs
            leds = [int(not led) for led in leds]
    
    def hold(self, beats, leds):
        self._append_step(leds, beats)

    def stop(self, beats):
        self._append_step(beats, [0] * 8)
    
    @property
    def steps(self):
        return self._steps

def pretty_print(steps):
    format_row = "{:>5}" * 2
    for step in steps:
        print(step.keys())
        # print(format_row.format(*step))

if __name__ == "__main__":
    leds = Blink()
    leds.blink([0,1,0,1,0,1,0,1], 2)
    leds.blink([1,0,1,0,1,0,1,0], 2, 2)
    leds.hold([1] * 8, 1)
    leds.stop(1)

    # print(leds.steps)
    # print(len(leds.steps))

    # https://blog.softhints.com/python-print-pretty-table-list/
    pretty_print(leds.steps)
