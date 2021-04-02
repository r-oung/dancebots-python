#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .waveform import sinewave
from ..core import Frame


def beats_to_bitstream(beat_times, sample_rate=44100):
    # Construct bitstream from a list of beat_times
    bitstream = []

    # Initialize indices
    beat_index = 0
    sample_index = 0

    # Create a tone
    tone = sinewave(1000, sample_rate)

    # Add beats to bitstream as long as there are beats
    while beat_index < len(beat_times):
        if (sample_index / float(sample_rate)) < beat_times[beat_index]:
            # Off beat
            bitstream.append(0)
            sample_index += 1
        else:
            # On beat
            bitstream += tone
            sample_index += len(tone)
            beat_index += 1

    return bitstream


def step_to_bitstream(step, sample_rate):
    seconds_per_beat = 1 # @TODO Remove this

    # Construct bitstream
    wav_samples = 0
    seconds_elapsed = 0
    seconds_per_step = step["beats"] * seconds_per_beat

    # Add composition to bitstream
    frames = []
    while frame.duration < seconds_per_step:
        frames.append(Frame(step["motor_l"], step["motor_r"], step["leds"], sample_rate))

    
    return frame.data


def composition_to_bitstream(composition, beat_times=None, sample_rate=44100):
    """
    Generate bitstream from composition
    Synchronize to beats if necessary
    """
    # Construct bitstream
    bitstream = Bitstream(sample_rate)

    # A. Beat synchronization not required
    if beat_times == None:
        # Add composition to bitstream
        for step in composition.steps:
            bs, ws = step_to_bitstream(step, sample_rate)
            bitstream += bs

        return bitstream
    
    # B. Beat synchronization is required
    # Get average seconds per beat
    # This is used to estimate the period of a step
    sum = 0
    for i in range(1, len(beat_times)):
        sum += beat_times[i] - beat_times[i - 1]
    seconds_per_beat = sum / (len(beat_times) - 1)

    # Initialize indices
    beat_index = 0
    wav_sample_index = 0
    composition_index = 0

    # Add composition to bitstream as long as there are beats
    while beat_index < len(beat_times):
        if (wav_sample_index / float(sample_rate)) < beat_times[beat_index]:
            # Off beat
            bitstream.append(0)
            wav_sample_index += 1
        else:
            # On beat
            if composition_index < len(composition.steps):
                step = composition.steps[composition_index]
                bs, ws = step_to_bitstream(step, seconds_per_beat)
                bitstream += bs
                wav_sample_index += ws
                composition_index += 1

            beat_index += 1

    return bitstream
