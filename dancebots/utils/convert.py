# -*- coding: utf-8 -*-
"""Conversion module.

"""
from .waveform import sinewave
from ..core import Frame, Bitstream


def step_to_frames(step, seconds_per_unit=1, sample_rate=44100):
    """Convert step to frames.

    Attributes:
            step: Step object.
            seconds_per_unit: Number of seconds per unit.
            sample_rate: Audio sampling rate (Hz).
    """
    seconds_per_step = step.num_units * seconds_per_unit

    frame = Frame(step.motor_l, step.motor_r, step.leds)
    bitstream = Bitstream([frame], sample_rate)
    repeat = int(seconds_per_step // bitstream.duration)  # floor division

    return [frame] * repeat


def steps_to_bitstream(steps, beat_times=None, sample_rate=44100):
    """Convert steps to bitstream.

    Attributes:
            step: Step object.
            beat_times: List of beat times (seconds).
            sample_rate: Audio sampling rate (Hz).
    """
    # A. No beat synchronization
    if beat_times is None:
        # Convert each step in a composition to a bitstream
        bitstream = Bitstream()
        for step in steps:
            frames = step_to_frames(step)
            bitstream += Bitstream(frames)

        return bitstream.bits

    # B. With beat synchronization
    # Get average seconds per beat
    # Used to estimate the period of a step
    total = 0
    for i in range(1, len(beat_times)):
        total += beat_times[i] - beat_times[i - 1]
    seconds_per_beat = total / (len(beat_times) - 1)

    # Initialize indices
    beat_index = 0
    step_index = 0
    bitstream = Bitstream()

    while beat_index < len(beat_times):
        time_index = len(bitstream) / float(sample_rate)
        if time_index < beat_times[beat_index]:
            # Off beat
            frame = Frame([0] * 8, [0] * 8, [0] * 8)
            bitstream += Bitstream([frame])
        else:
            # On beat
            # @TODO Only taking one step, but it should take multiple steps if beat < 1
            if step_index < len(steps):
                frames = step_to_frames(steps[step_index], seconds_per_beat)
                bitstream += Bitstream(frames)
                step_index += 1

            beat_index += 1

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
