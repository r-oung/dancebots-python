#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""I/O module.

"""
import wave
import struct
import librosa
# import youtube_dl as yt

def load(filename):
    """Load audio file.

    Attribute:
            filename: Path to audio file.
    """
    # Load audio file without any modifications to the sampling rate
    # https://librosa.org/doc/latest/generated/librosa.load.html
    audio, sample_rate = librosa.load(filename, sr=None, mono=False)
    print(
        "\nSampling rate: {} Hz | Channels: {} | Samples: {}".format(
            sample_rate, audio.shape[0], audio.shape[1]
        )
    )
    return audio, sample_rate


# https://realpython.com/python-print/
def create_wav(channel_l, channel_r, filename="output.wav", sample_rate=44100):
    """Create wave-file from time-series data.

    Attribute:
            channel_l: Left channel time-series.
            channel_r: Right channel time-series.
            filename: Output filename.
            sample_rate: Audio sampling rate (Hz).
    """
    if len(channel_l) != len(channel_r):
        raise ValueError(
            "Left and right channel lists must be of equal length: ({}, {})".format(
                len(channel_l), len(channel_r)
            )
        )

    with wave.open(filename, "w") as wav_file:
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

    return


# def get_youtube(url):
#     options = {
#         "format": "bestaudio/best",
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192",
#             }
#         ],
#     }

#     with yt.YoutubeDL(options) as ytdl:
#         print ("Downloading: {}".format(url))
#         ytdl.download([url])

#     return
