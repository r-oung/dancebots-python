"""Plot audio file.

"""
import dancebots.utils as utils

# Load audio file
audio, sample_rate = utils.load("../data/motor_test.mp3")

# Visualize audio file
utils.plot(
    channel_l=audio[0],
    channel_r=audio[1],
    sample_rate=sample_rate,
    xlim=[0.051, 0.069]
)
