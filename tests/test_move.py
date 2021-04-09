#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots as db
from dancebots.core import Move
import dancebots.utils as utils

# 1. Check bit order
move = Move()
motor_l, motor_r = move.forward(1, 100)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.forward(1, 50)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.forward(1, 0)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.forward(1)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.backward(1, 100)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.backward(1, 50)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.backward(1, 0)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.backward(1)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.left(1, 100)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.left(1, 50)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.left(1, 0)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.left(1)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.right(1, 100)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.right(1, 50)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.right(1, 0)
print("{} {}".format(motor_l, motor_r))

move.clear()
motor_l, motor_r = move.right(1)
print("{} {}".format(motor_l, motor_r))


# # 2. Print moves
# move = Move("seconds")
# move.forward(5)
# move.backward(4)
# move.left(3)
# move.right(2)
# move.stop(1)
# print(move)

# 3.
# composition = Compose(move, None)
# frames = utils.convert.composition_to_frames(composition, None)
# print(frames.length)

# db.insert(move)
# db.save()
# db.plot()
