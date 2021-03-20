#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa

def get_beats(filename):
    # Load song file
    y, sr = librosa.load(filename)

    # Separate harmonics and percussives into two waveforms
    y_harm, y_perc = librosa.effects.hpss(y)

    # Beat track on the percussive signal
    bpm, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sr)

    # Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return bpm, beat_times

if __name__ == "__main__":
    bpm, beat_times = get_beats("../samples/daft_punk.mp3")

    # Output to console
    print(beat_times)
    print('Estimated tempo: {:.2f} BPM'.format(bpm))
