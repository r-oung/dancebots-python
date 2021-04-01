#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots as db
from dancebots import Move, Light

# Choreograph moves
move = Move()
for i in range(5):
  move.forward(1)
  move.backward(1)
move.left(5)
move.right(5)
move.stop(1)

# Choreograph lights
light = Light()
light.blink([0,1,0,1,0,1,0,1], 5)
light.blink([1,0,1,0,1,0,1,0], 5)
light.hold([1,0,1,0,1,0,1,0], 2)
light.stop(1)

# Construct dancebot music file
db.load("./samples/dance_demo.mp3") # load music
db.insert(move) # insert moves
db.insert(light) # insert lights
db.save("my_dance_file.wav") # save to disk
db.plot() # plot
