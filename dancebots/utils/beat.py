# -*- coding: utf-8 -*-
"""Beat module.

"""
import librosa


def get_beats(audio, sample_rate):
    """Get beat times from audio data

    Attributes:
            audio: librosa audio data format.
            sample_rate: Audio data sampling rate (Hz).
    """
    # Convert to mono
    mono = librosa.to_mono(audio)

    # Separate harmonics and percussives into two waveforms
    _, y_perc = librosa.effects.hpss(mono)

    # Beat track on the percussive signal
    bpm, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sample_rate)
    # bpm, beat_frames = librosa.beat.beat_track(y=mono, sr=sample_rate)

    # Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sample_rate)

    return bpm, beat_times
