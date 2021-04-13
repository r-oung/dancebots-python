"""Dancebots package.

Package to script movement and lights for a DanceBot.
"""
from . import core
from . import utils

from .core import Move
from .core import Light

# pylint: disable=C0103
# pylint: disable=W0603

# Global variables
audio = []
sample_rate = 44100
beat_times = None
moves = []
lights = []
channel_l = []
channel_r = []


def load(filename):
    """Load audio file.

    Attributes:
            filename: Path to audio file.
    """
    global audio, sample_rate
    global channel_l, channel_r
    global beat_times

    # Load audio file
    print("Loading audio file: {}".format(filename))
    audio, sample_rate = utils.load(filename)

    # Extract beats
    print("Extracting beats...(be patient)")
    bpm, beat_times = utils.get_beats(audio, sample_rate)
    print("Estimated tempo: {:.2f} BPM".format(bpm))

    # Keep data in a buffer for plotting purposes
    channel_l = audio[0]
    channel_r = audio[1]


def add(obj):
    """Add composition element.

    Attributes:
            obj: Can either be an object of type Move or Light.
    """
    global moves, lights

    if isinstance(obj, Move):
        moves.append(obj)
    elif isinstance(obj, Light):
        lights.append(obj)
    else:
        raise ValueError("Invalid argument")


def save(filename="output.wav", audio_channel="left"):
    """Save composition.

    Attributes:
            filename: Path to output audio file.
            audio_channel: Select which channel to use for audio ("left" or "right")
    """
    global audio, sample_rate
    global channel_l, channel_r
    global beat_times

    print("Composing choreography")
    composition = core.Compose(moves, lights)
    bitstream = utils.convert.steps_to_bitstream(
        composition.steps, beat_times, sample_rate
    )

    if len(audio) == 0:
        # Audio data does not exist
        # Duplicate bitstream on audio channel
        channel_l = bitstream
        channel_r = bitstream
    else:
        # Audio data exists
        # Make composition-bitstream the same length as the audio channel
        if len(bitstream) > audio.shape[1]:
            # trim bitstream to the same length as the audio
            bitstream = bitstream[: audio.shape[1] :]
        else:
            # append zeros to the end of the bitstream to make it the same length as the audio
            bitstream += [0] * (audio.shape[1] - len(bitstream))

        # Copy data to the selected audio channel
        if audio_channel == "left":
            channel_l = audio[0]
            channel_r = bitstream
        elif audio_channel == "right":
            channel_l = bitstream
            channel_r = audio[1]
        else:
            raise ValueError("Invalid audio channel")

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
    """Plot time-series data."""
    global channel_l, channel_r
    global beat_times

    if len(channel_l) == 0 or len(channel_r) == 0:
        raise ValueError("You must first load and/or save an audio file")

    if beat_times is None:
        utils.plot(channel_l=channel_l, channel_r=channel_r, sample_rate=sample_rate)
    else:
        utils.plot(
            channel_l=channel_l,
            channel_r=channel_r,
            sample_rate=sample_rate,
            xlim=[beat_times[0], beat_times[0] + 1],
        )
