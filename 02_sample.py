#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots as db
from dancebots import Move, Light

# Create a move
move = Move()
for i in range(5):  # repeat the following 5 times
    move.left(1)  # move left for 1 beat
    move.right(1)  # move right for 1 beat

# Add some lights
light = Light()
light.blink(
    [0, 1, 0, 1, 0, 1, 0, 1], 5
)  # each element in the list represents a single LED (0 is OFF, 1 is ON), blink for 5 beats
light.blink([1, 0, 1, 0, 1, 0, 1, 0], 5)  # blink for 5 beats
light.hold([1, 0, 1, 0, 1, 0, 1, 0], 2)  # hold for 2 beats

# Construct dancebot audio file
db.load(
    "./samples/dance_demo.mp3"
)  # load music file, which will automatically extract beats
db.add(move)  # add moves
db.add(light)  # add lights
db.save("02_sample.wav")  # save to disk

# Visualize the audio file
db.plot()
