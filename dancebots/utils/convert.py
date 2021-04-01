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


def composition_to_bitstream(composition, beat_times, sample_rate=44100):
    """
    Synchronize composition to beat-times
    and generate bitstream
    """
    # Construct bitstream
    bitstream = []

    # Get average seconds per beat
    sum = 0
    for i in range(1, len(beat_times)):
        sum += beat_times[i] - beat_times[i - 1]
    seconds_per_beat = sum / (len(beat_times) - 1)

    # Initialize indices
    beat_index = 0
    sample_index = 0
    composition_index = 0

    # Add composition to bitstream as long as there are beats
    while beat_index < len(beat_times):
        if (sample_index / float(sample_rate)) < beat_times[beat_index]:
            # Off beat
            bitstream.append(0)
            sample_index += 1
        else:
            # On beat
            if composition_index < len(composition.steps):
                step = composition.steps[composition_index]
                seconds_elapsed = 0
                seconds_per_step = step["beats"] * seconds_per_beat

                while seconds_elapsed < seconds_per_step:
                    frame = Frame(
                        motor_l=step["motor_l"],
                        motor_r=step["motor_r"],
                        leds=step["leds"],
                        sample_rate=sample_rate,
                    )
                    bitstream += frame.bitstream
                    sample_index += frame.length
                    seconds_elapsed += frame.duration

                composition_index += 1

            beat_index += 1

    return bitstream


def composition_to_bitstream2(composition, seconds_per_beat=1):
    """Generate bitstream from composition (no beat syncing)"""
    # Construct bitstream
    bitstream = []

    # Add composition to bitstream as long as there are beats
    for step in composition.steps:
        seconds_elapsed = 0
        seconds_per_step = step["beats"] * seconds_per_beat

        while seconds_elapsed < seconds_per_step:
            frame = Frame(
                motor_l=step["motor_l"],
                motor_r=step["motor_r"],
                leds=step["leds"],
            )
            bitstream += frame.bitstream
            seconds_elapsed += frame.duration

    return bitstream
