from . import core
from . import utils

from .core.move import Move

# Convenience functions

def load(filename):
    global y, sr
    global bpm, beat_times

    # Load audio file
    y, sr = utils.inout.load(filename)
    
    # Extract beats
    bpm, beat_times = utils.beat.get_beats(y, sr)

def sync(frames):
    global ch_l, ch_r
    # @TODO
    pass

def plot():
    utils.plot(y, sr)

def save(filename="output.wav"):
    utils.convert.bitstream_to_wav(ch_l, ch_r, filename, 44100)