#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots import Move, Light, Compose


move1 = Move()
move1.forward(3)
move1.backward(3)
move1.stop(1)

move2 = Move()
move2.left(3)
move2.right(3)
move2.stop(1)

light1 = Light()
light1.blink([0, 1, 0, 1, 0, 1, 0, 1], 3, 4)
light1.blink([1, 1, 0, 0, 1, 1, 0, 0], 3, 3)
light1.stop(1)

light2 = Light()
light2.hold([1] * 8, 4)
light2.blink([1, 0, 1, 0, 1, 0, 1, 0], 3, 5)


# Moves only
composition = Compose(moves=[move1, move2])
print(composition)


# Lights only
composition = Compose(lights=[light1, light2])
print(composition)


# Moves and Lights
composition = Compose([move1, move2], [light1, light2])
print(composition)

composition = Compose([move1], [light1, light2])
print(composition)

composition = Compose([move1, move2], [light1])
print(composition)
