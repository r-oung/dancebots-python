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


def step_to_frames(step, sample_rate=44100):
    seconds_per_beat = 1 # @TODO Remove this

    # Construct bitstream
    seconds_per_step = step["beats"] * seconds_per_beat

    # Add composition to bitstream
    frame = Frame(step["motor_l"], step["motor_r"], step["leds"], sample_rate)
    while frame.duration < seconds_per_step:
        frame += frame
    
    return frame


def composition_to_frames(composition, beat_times=None, sample_rate=44100):
    """
    Generate bitstream from composition
    Synchronize to beats if necessary
    """
    frame = None

    # A. Beat synchronization not required
    if beat_times == None:
        # Convert composition to frames
        for step in composition.steps:
            if frame == None:
                frame = step_to_frames(step, sample_rate)
            else:
                frame += step_to_frames(step, sample_rate)

        return frame
    
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
                if frame == None:
                    frame = step_to_frames(step, seconds_per_beat)
                else:
                    frame += step_to_frames(step, seconds_per_beat)
                wav_sample_index = frame.length
                composition_index += 1

            beat_index += 1

    return frame
