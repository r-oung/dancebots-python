#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Frame
import dancebots.utils.plot as plot

# Set the individual bits for the motors and LEDs
motor_l = [0, 1, 0, 0, 1, 1, 0, 1]
motor_r = [0, 1, 0, 0, 1, 1, 0, 1]
leds = [0] * 8
frame = Frame(motor_l, motor_r, leds)

frames = [frame] * 100

# Print the complete frame
print(frame)

# Visualize the frame
plot(channel_l=frames, channel_r=None, sample_rate=44100, xlim=[0.051, 0.069])
