#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Blink:
    """Blink"""

    def __init__(self):
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
        for i in range(num_steps):
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
    
    # https://realpython.com/python-print/
    def __str__(self):
        return self._steps
    
    def __repr__(self):
        return f"Blink('{self._max_freq}')"

def pprint(steps):
    # @TODO Integrate with __str__
    # https://blog.softhints.com/python-print-pretty-table-list/
    print()
    header = ['Step', 'LEDs', 'Beats']
    format_row = "{:<6} {:<26} {:<7}"
    print(format_row.format(*header))

    for num, step in enumerate(steps, start=1):
        print(format_row.format(num, str(step['leds']), step['beats']))

    print()

if __name__ == "__main__":
    leds = Blink()
    leds.blink([0,1,0,1,0,1,0,1], 2, 4)
    leds.blink([1,0,1,0,1,0,1,0], 2, 2)
    leds.hold([1] * 8, 4)
    leds.stop(1)

    pprint(leds.steps)
