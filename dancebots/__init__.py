from . import core
from . import utils

from .core.move import Move

# Convenience functions

def load(filename):
    global y, sr
    global bpm, beat_times

    # Load audio file
    print('Loading audio file: {}'.format(filename))
    y, sr = utils.inout.load(filename)
    
    # Extract beats
    print('Extracting beats...')
    bpm, beat_times = utils.beat.get_beats(y, sr)
    print('Estimated tempo: {:.2f} BPM'.format(bpm))


def metronome(filename='output.wav', beat_ch='right'):
    # Construct metronome bitstream
    bitstream = utils.beat.metronome(y, sr, beat_times)

    # Construct WAV file
    print('Constructing audio file...')
    if (beat_ch == 'right'):
        utils.convert.bitstream_to_wav(ch_l=y[0], ch_r=bitstream, filename=filename)
    elif (beat_ch == 'left'):
        utils.convert.bitstream_to_wav(ch_l=bitstream, ch_r=y[1], filename=filename)

    print('Done')


def sync(frames):
    global ch_l, ch_r
    # @TODO
    pass

def plot():
    utils.plot(y, sr)

def save(filename="output.wav"):
    utils.convert.bitstream_to_wav(ch_l, ch_r, filename, 44100)