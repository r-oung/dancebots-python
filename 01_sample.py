#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots as db
from dancebots import Move

# Move the robot
move = Move("seconds") # Use 'seconds' as units. Options are "seconds" or "beats" (default)
move.forward(3) # move forward for 3 seconds
move.backward(3) # move backward for 3 seconds
move.left(2) # turn left for 2 seconds
move.right(2) # turn right for 2 seconds

# Print to sequence of moves
print(move)

# Build audio file
db.add(move) # add move
db.save("01_sample.wav") # save to disk
db.plot() # visualize the audio file
