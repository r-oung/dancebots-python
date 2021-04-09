#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Frame
import dancebots.utils as utils

motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
leds = [1, 0, 1, 0, 1, 0, 1, 0]
frame1 = Frame(motor_l, motor_r, leds)

motor_l = [0, 0, 0, 0, 1, 1, 1, 1]
motor_r = [0, 0, 1, 1, 0, 0, 1, 1]
leds = [0, 1, 0, 1, 0, 1, 0, 1]
frame2 = Frame(motor_l, motor_r, leds)

# 1. Single frames
print(frame1)
print(frame2)
utils.plot(channel_l=frame1.bits, channel_r=frame2.bits)

# # 2. Sum
# sum = frame1 + frame2
# print(sum)
# utils.plot(channel_l=sum.bits, channel_r=sum.bits)

# # 2. Sum Reverse
# sum = frame2 + frame1
# print(sum)
# utils.plot(channel_l=sum.bits, channel_r=sum.bits)

# # 4. Sum list
# sum = sum([frame1, frame2])
# print(sum)
# utils.plot(channel_l=sum.bits, channel_r=sum.bits)

# # 5. Sum list reverse
# sum = sum([frame2, frame1])
# print(sum)
# utils.plot(channel_l=sum.bits, channel_r=sum.bits)
