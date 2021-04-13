#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Visualize frame.

"""
from dancebots.core import Frame
import dancebots.utils.plot as plot

# Set the individual bits for the motors and LEDs
motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
leds = [1, 0, 1, 0, 1, 0, 1, 0]
frame = Frame(motor_l, motor_r, leds)

# Print the complete frame
print(frame)

# Visualize the frame
plot(frame)
