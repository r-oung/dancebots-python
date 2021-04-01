#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa


def get_beats(audio, sample_rate):
    # Convert to mono
    mono = librosa.to_mono(audio)

    # Separate harmonics and percussives into two waveforms
    y_harm, y_perc = librosa.effects.hpss(mono)

    # Beat track on the percussive signal
    bpm, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sample_rate)
    # bpm, beat_frames = librosa.beat.beat_track(y=mono, sr=sample_rate)

    # Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)

    return bpm, beat_times


if __name__ == "__main__":
    from inout import load

    # Load song file
    audio, sample_rate = load("../../samples/dance_demo.mp3")

    # Get beats
    bpm, beat_times = get_beats(audio, sample_rate)
    print("Number of beats: {}".format(len(beat_times)))
    print("Estimated tempo: {:.2f} BPM".format(bpm))
