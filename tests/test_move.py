#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots as db
from dancebots.core import Move


# Check bit order
move = Move()

motor_l, motor_r = move.forward(1, 100)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [1, 1, 1, 1, 1, 1, 1, 1]
assert motor_r == [1, 1, 1, 1, 1, 1, 1, 1]

move.clear()
motor_l, motor_r = move.forward(1, 50)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 1, 1]
assert motor_r == [0, 0, 0, 0, 0, 0, 1, 1]

move.clear()
motor_l, motor_r = move.forward(1, 0)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 0, 1]
assert motor_r == [0, 0, 0, 0, 0, 0, 0, 1]

move.clear()
motor_l, motor_r = move.backward(1, 100)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [1, 1, 1, 1, 1, 1, 1, 0]
assert motor_r == [1, 1, 1, 1, 1, 1, 1, 0]

move.clear()
motor_l, motor_r = move.backward(1, 50)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 1, 0]
assert motor_r == [0, 0, 0, 0, 0, 0, 1, 0]

move.clear()
motor_l, motor_r = move.backward(1, 0)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 0, 0]
assert motor_r == [0, 0, 0, 0, 0, 0, 0, 0]

move.clear()
motor_l, motor_r = move.left(1, 100)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [1, 1, 1, 1, 1, 1, 1, 0]
assert motor_r == [1, 1, 1, 1, 1, 1, 1, 1]

move.clear()
motor_l, motor_r = move.left(1, 50)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 1, 0]
assert motor_r == [0, 0, 0, 0, 0, 0, 1, 1]

move.clear()
motor_l, motor_r = move.left(1, 0)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 0, 0]
assert motor_r == [0, 0, 0, 0, 0, 0, 0, 1]

move.clear()
motor_l, motor_r = move.right(1, 100)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [1, 1, 1, 1, 1, 1, 1, 1]
assert motor_r == [1, 1, 1, 1, 1, 1, 1, 0]

move.clear()
motor_l, motor_r = move.right(1, 50)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 1, 1]
assert motor_r == [0, 0, 0, 0, 0, 0, 1, 0]

move.clear()
motor_l, motor_r = move.right(1, 0)
print("{} {}".format(motor_l, motor_r))
assert motor_l == [0, 0, 0, 0, 0, 0, 0, 1]
assert motor_r == [0, 0, 0, 0, 0, 0, 0, 0]
