# -*- coding: utf-8 -*-
"""Beat extraction module

Extracts beat information from an audio file.

Copyright (C) 2021-2022 Raymond Oung

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


def get_beats(audio, sample_rate):
    """Get beat times from audio data

    Attributes:
            audio: librosa audio data format.
            sample_rate: Audio data sampling rate (Hz).
    """
    # pylint: disable=C0415
    import librosa

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
