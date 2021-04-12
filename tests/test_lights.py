#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots.utils as utils
from dancebots.core import Light


# 1. Prints lights
light = Light()
light.blink([1, 0, 1, 0, 1, 0, 1, 0], 3, 2)
light.hold([1, 1, 0, 0, 1, 1, 0, 0], 2)
light.stop(1)
print(light)

for step in light.steps:
    print(step.leds)
