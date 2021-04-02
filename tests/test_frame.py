#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Frame
import dancebots.utils as utils


# # 1. Single frame
# motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
# motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
# leds = [1, 0, 1, 0, 1, 0, 1, 0]
# frame = Frame(motor_l, motor_r, leds)

# utils.plot(channel_l=frame.data, channel_r=frame.data)


# # 2. Add
# motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
# motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
# leds = [1, 0, 1, 0, 1, 0, 1, 0]

# a = Frame(motor_l, motor_r, leds)
# b = Frame(motor_l, motor_r, leds)

# c = a + b
# utils.plot(channel_l=c.data, channel_r=c.data)


# 3. Sum list
motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
leds = [1, 0, 1, 0, 1, 0, 1, 0]

a = Frame(motor_l, motor_r, leds)
b = Frame(motor_l, motor_r, leds)

c = sum([a, b])
utils.plot(channel_l=c.data, channel_r=c.data)
