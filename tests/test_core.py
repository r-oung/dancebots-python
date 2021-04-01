#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dancebots import Move, Light, Compose

move = Move()
move.forward(5, 100)
move.backward(5, 100)
move.left(5, 100)
move.right(5, 100)
move.stop(1)

light = Light()
light.blink([0, 1, 0, 1, 0, 1, 0, 1], 2, 4)
light.blink([1, 0, 1, 0, 1, 0, 1, 0], 2, 2)
light.hold([1] * 8, 4)
light.stop(1)

choreography = Compose(move, light)
print(choreography)
