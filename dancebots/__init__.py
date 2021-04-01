from . import core
from . import utils

from .core import Move
from .core import Light
from .core import Compose

# Convenience functions
moves = None
lights = None

def load(filename):
    global audio, sample_rate
    global beat_times

    # Load audio file
    print("Loading audio file: {}".format(filename))
    audio, sample_rate = utils.load(filename)

    # Extract beats
    print("Extracting beats...")
    bpm, beat_times = utils.get_beats(audio, sample_rate)
    print("Estimated tempo: {:.2f} BPM".format(bpm))


def insert(obj):
    if isinstance(obj, Move):
        moves = obj
  
    elif isinstance(obj, Light):
        lights = obj

    else:
        raise ValueError("Invalid argument")


def plot():
    utils.plot(channel_l=audio[0], channel_r=bitstream, sample_rate=sample_rate)


def save(filename="output.wav", audio_channel="left"):
    global bitstream

    print("Composing choreography")
    composition = Compose(moves, lights)
    #@TODO Consolidate 2 different composition functions
    bitstream = utils.convert.composition_to_bitstream(
        composition, beat_times, sample_rate
    )

    # Make composition-bitstream the same length as audio channel
    if len(bitstream) > audio.shape[1]:
        bitstream = bitstream[: audio.shape[1] :]
    else:
        bitstream += [0] * (audio.shape[1] - len(bitstream))


    print("Constructing audio file...")
    if audio_channel == "left":
        utils.create_wav(
            channel_l=audio[0],
            channel_r=bitstream,
            filename=filename,
            sample_rate=sample_rate,
        )
    elif audio_channel == "right":
        utils.create_wav(
            channel_l=bitstream,
            channel_r=audio[1],
            filename=filename,
            sample_rate=sample_rate,
        )

    print("Done")
