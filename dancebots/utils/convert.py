# -*- coding: utf-8 -*-
"""Conversion module.

"""
from .waveform import sinewave
from ..core import Frame, Bitstream


def steps_to_bitstream(steps, beat_times=None, sample_rate=44100):
    """Convert steps to bitstream.

    Attributes:
            step: Step object.
            beat_times: List of beat times (seconds).
            sample_rate: Audio sampling rate (Hz).
    """
    # A. No beat synchronization
    # Let 1 unit = 1 second
    if beat_times is None:
        # Convert each step in a composition to a bitstream
        bitstream = Bitstream()
        for step in steps:
            frame = Frame(step.motor_l, step.motor_r, step.leds)
            repeat = int(step.num_units // Bitstream([frame], sample_rate).duration)
            bitstream += Bitstream([frame] * repeat)

        return bitstream.bits

    # B. With beat synchronization
    bitstream = Bitstream()

    # Pad with empty frames until the first beat
    while (len(bitstream) / float(sample_rate)) < beat_times[0]:
        frame = Frame([0] * 8, [0] * 8, [0] * 8)
        bitstream += Bitstream([frame])

    # Insert steps that are synchronized to beats
    beat_index = 1
    end_step = beat_times[0]
    for step in steps:
        if beat_index < len(beat_times):
            # Estimate when step should end
            end_step += step.num_units * (
                beat_times[beat_index] - beat_times[beat_index - 1]
            )

            # Insert step
            while (len(bitstream) / float(sample_rate)) < end_step:
                frame = Frame(step.motor_l, step.motor_r, step.leds)
                bitstream += Bitstream([frame], sample_rate)

            # Check if beat index should be incremented
            if (len(bitstream) / float(sample_rate)) > beat_times[beat_index]:
                beat_index += 1
        else:
            # No more beats
            break

    return bitstream.bits


def beats_to_bitstream(beat_times, sample_rate=44100):
    """Convert beats to bitstream.

    Attributes:
            beat_times: List of beat times (seconds).
            sample_rate: Audio sampling rate (Hz).
    """
    # Construct bitstream from a list of beat_times
    bitstream = []

    # Initialize indices
    beat_index = 0

    # Create a tone
    tone = sinewave(1000, sample_rate)

    # Step through each beat
    while beat_index < len(beat_times):
        time_index = len(bitstream) / float(sample_rate)
        if time_index < beat_times[beat_index]:
            # Off beat
            bitstream.append(0)
        else:
            # On beat
            bitstream += tone
            beat_index += 1

    return bitstream
