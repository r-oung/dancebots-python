"""Visualize frames.

"""
from dancebots.core import Frame
import dancebots.utils.plot as plot

# Create a single frame
motor_l = [0, 1, 0, 0, 1, 1, 0, 1]
motor_r = [0, 1, 0, 0, 1, 1, 0, 1]
leds = [0] * 8
frame = Frame(motor_l, motor_r, leds)

# Repeat frames
frames = [frame] * 100

# Print a single frame
print(frame)

# Visualize frames
plot(frames)
