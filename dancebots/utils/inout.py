# -*- coding: utf-8 -*-
"""File import/export module

Functions for importing and exporting audio files.

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
import wave
import struct


def load(filename):
    """Load audio file.

    Attributes:
            filename: Path to audio file.
    """
    # pylint: disable=C0415
    import librosa

    # Load audio file without any modifications to the sampling rate
    # https://librosa.org/doc/latest/generated/librosa.load.html
    audio, sample_rate = librosa.load(filename, sr=None, mono=False)
    print(
        "\nSampling rate: {} Hz | Channels: {} | Samples: {}".format(
            sample_rate, audio.shape[0], audio.shape[1]
        )
    )
    return audio, sample_rate


def create_wav(channel_l, channel_r, filename="output.wav", sample_rate=44100):
    """Create wave-file from time-series data.

    Attributes:
            channel_l: Left channel time-series.
            channel_r: Right channel time-series.
            filename: Output filename.
            sample_rate: Audio sampling rate (Hz).
    """
    if len(channel_l) != len(channel_r):
        raise ValueError(
            "👎 Left and right channel lists must be of equal length: ({}, {})".format(
                len(channel_l), len(channel_r)
            )
        )

    with wave.open(filename, "w") as wav_file:
        # pylint: disable=E1101
        wav_file.setnchannels(2)  # number of channels
        wav_file.setsampwidth(2)  # sample width [bytes]
        wav_file.setframerate(sample_rate)  # frame-rate [Hz]
        wav_file.setnframes(len(channel_l))  # total number of audio frames
        wav_file.setcomptype("NONE", "Not compressed")  # no compression

        # WAV file here is using short (16-bit) signed integers
        # So we multiply each bit by 32767 to get the maximum value
        binary_list = []
        for i, _ in enumerate(channel_l):
            # left-channel
            binary_data = struct.pack("h", int(channel_l[i] * 32767.0))
            binary_list.append(binary_data)

            # right-channel
            binary_data = struct.pack("h", int(channel_r[i] * 32767.0))
            binary_list.append(binary_data)

        binary_string = b"".join(binary_list)
        wav_file.writeframes(binary_string)
