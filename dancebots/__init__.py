from . import core
from . import utils

from .core import Move
from .core import Light
from .core import Compose

# Global variables
audio = None
sample_rate = 44100
beat_times = None
moves = None
lights = None
channel_l = []
channel_r = []

def load(filename):
    global audio
    global sample_rate
    global beat_times

    # Load audio file
    print("Loading audio file: {}".format(filename))
    audio, sample_rate = utils.load(filename)

    # Extract beats
    print("Extracting beats...")
    bpm, beat_times = utils.get_beats(audio, sample_rate)
    print("Estimated tempo: {:.2f} BPM".format(bpm))


def insert(obj):
    global moves
    global lights

    # @TODO Allow for any number of inserts
    if isinstance(obj, Move):
        moves = obj
        print("Added")
    elif isinstance(obj, Light):
        lights = obj
    else:
        raise ValueError("Invalid argument")


def save(filename="output.wav", audio_channel="left"):
    global channel_l
    global channel_r

    print("Composing choreography")
    composition = Compose(moves, lights)
    bitstream = utils.convert.composition_to_bitstream(
        composition, beat_times, sample_rate
    )
    
    if audio != None:
        # Audio data exists
        # Make composition-bitstream the same length as audio channel
        if len(bitstream) > audio.shape[1]:
            bitstream = bitstream[: audio.shape[1] :]
        else:
            bitstream += [0] * (audio.shape[1] - len(bitstream))

        # Buffer data from selected audio channel
        if audio_channel == "left":
            channel_l = audio[0]
            channel_r = bitstream
        elif audio_channel == "right":
            channel_l = bitstream
            channel_r = audio[1]
    else:
        # Audio data does not exist
        # Duplicate bitstream on audio channel
        channel_l = bitstream
        channel_r = bitstream

    print("Constructing audio file...")
    utils.create_wav(
        channel_l=channel_l,
        channel_r=channel_r,
        filename=filename,
        sample_rate=sample_rate,
    )
    print("Done")

    return {
        "channel_l": channel_l,
        "channel_r": channel_r,
    }


def plot():
    global channel_l
    global channel_r
    
    utils.plot(channel_l=channel_l, channel_r=channel_r, sample_rate=sample_rate)
