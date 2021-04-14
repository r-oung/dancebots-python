"""Create a simple dance composition.

"""
import dancebots as db
from dancebots import Move, Light

# Create a move
twist = Move()  # call the move 'twist'
for i in range(10):  # repeat the following 10 times
    twist.left(1)  # move left for 1 beat
    twist.right(1)  # move right for 1 beat

# Add some lights
light = Light()

# Each element in the list represents a single LED (OFF=0, ON=1)
light.blink([1, 1, 1, 1, 1, 1, 1, 1], 10, 5)  # blink for 10 beats at 5 Hz
light.hold([1, 1, 1, 1, 1, 1, 1, 1], 2)  # keep LEDs on for 2 beats

# Build audio file
db.load("../data/sample.wav")  # load music file
db.add(twist)  # add moves
db.add(light)  # add lights
db.save("02_example.wav")  # save to disk

# Visualize audio file
db.plot()
