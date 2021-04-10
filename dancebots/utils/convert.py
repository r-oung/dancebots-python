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


def step_to_frames(step, seconds_per_unit=1, sample_rate=44100):
    seconds_per_step = step.num_units * seconds_per_unit

    frames = None
    while frames.duration < seconds_per_step:
        if frames == None:
            frames = Frame(step.motor_l, step.motor_r, step.leds, sample_rate)
        else:
            frames += frames
    
    return frames


def steps_to_bitstream(steps, beat_times=None, sample_rate=44100):
    """
    Generate frames
    Synchronize to beats if necessary
    """
    frames = None

    # A. Beat synchronization not required
    if beat_times == None:
        # Convert composition to frames
        for step in composition.steps:
            if frames == None:
                frames = step_to_frames(step, sample_rate)
            else:
                frames += step_to_frames(step, sample_rate)

        return frames.bits
    
    # B. Beat synchronization is required
    # Get average seconds per beat
    # Used to estimate the period of a step
    sum = 0
    for i in range(1, len(beat_times)):
        sum += beat_times[i] - beat_times[i - 1]
    seconds_per_beat = sum / (len(beat_times) - 1)

    # Initialize indices
    beat_index = 0
    step_index = 0
    bitstream = []

    # Add composition to bitstream as long as there are beats
    while beat_index < len(beat_times):
        if (len(bitstream) / float(sample_rate)) < beat_times[beat_index]:
            # Off beat
            bitstream += [0]
        else:
            # On beat
            if step_index < len(steps):
                current_step = steps[step_index]
                if frame == None:
                    frame = step_to_frames(current_step, seconds_per_beat)
                else:
                    frame += step_to_frames(current_step, seconds_per_beat)
                
                bitstream += frame.bits
                step_index += 1

            beat_index += 1

    return bitstream
