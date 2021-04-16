"""Create a simple dance composition.

"""
import dancebots as db
from dancebots import Move, Light

# Create a move
move = Move()
for _ in range(10):  # repeat the following 10 times
    move.left(1)  # move left for 1 beat
    move.right(1)  # move right for 1 beat

# Add some lights
light = Light()

# Each element in the list represents a single LED (OFF=0, ON=1)
light.blink([1, 1, 1, 1, 1, 1, 1, 1], 10, 4)  # blink for 10 beats at 4 Hz

# Build audio file
db.load("../data/sample.wav")  # load music file
db.add(move)  # add moves
db.add(light)  # add lights
db.save("dance_basic.wav")  # save to disk

# Visualize audio file
db.plot()
