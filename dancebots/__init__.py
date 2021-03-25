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


def metronome(filename='output.wav', beat_channel='right'):
    # Construct metronome bitstream
    bitstream = utils.beat.metronome(y, sr, beat_times)

    # Save file
    save(filename, beat_times)


def sync(moves, leds):
    global bitstream = []
    beat_fraction = 4 # Constant
    frames = [{}] * len(y) * beat_fraction
    
    i = 0
    
    # Step through MOVES
    for move in moves:
        for beat in move['beats']:
            for fraction in range(beat_fraction):
                frames[i] = {
                    'left_motor': move['left_motor'],
                    'right_motor': move['right_motor'],
                }
                i += 1

    # @TODO LEDS

    # Convert choreography to bitstream
    for frame in frames:
        f = Frame() # @TODO create frame in the constructor
        f.create(frame)
        bitstream += f.bitstream


def plot():
    utils.plot(y, sr)


def save(filename="output.wav", beat_channel='right'):
    print('Constructing audio file...')
    if (beat_channel == 'right'):
        utils.convert.bitstream_to_wav(ch_l=y[0], ch_r=bitstream, filename=filename, sr=sr)
    elif (beat_channel == 'left'):
        utils.convert.bitstream_to_wav(ch_l=bitstream, ch_r=y[1], filename=filename, sr=sr)

    print('Done')