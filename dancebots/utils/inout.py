#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa
import wave
import struct

# import youtube_dl as yt


def load(filename):
    # Load audio file without any modifications
    # https://librosa.org/doc/latest/generated/librosa.load.html
    audio, sample_rate = librosa.load(filename, sr=None, mono=False)
    print(
        "Sampling rate: {} Hz | Channels: {} | Samples: {}".format(
            sample_rate, audio.shape[0], audio.shape[1]
        )
    )
    return audio, sample_rate


# https://realpython.com/python-print/
def create_wav(channel_l, channel_r, filename="output.wav", sample_rate=44100):
    if len(channel_l) != len(channel_r):
        raise ValueError(
            "Left and right channel lists must be of equal length: ({}, {})".format(
                len(channel_l), len(channel_r)
            )
        )

    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(2)  # number of channels
        wav_file.setsampwidth(2)  # sample with [bytes]
        wav_file.setframerate(sample_rate)  # frame-rate [Hz]
        wav_file.setnframes(len(channel_l))
        wav_file.setcomptype("NONE", "Not compressed")  # compression type

        # WAV file here is using short (16-bit) signed integers
        # So we multiply each bit by 32767 to get the maximum value
        bin_list = []
        for i in range(len(channel_l)):
            # left-channel
            bin_data = struct.pack("h", int(channel_l[i] * 32767.0))
            bin_list.append(bin_data)

            # right-channel
            bin_data = struct.pack("h", int(channel_r[i] * 32767.0))
            bin_list.append(bin_data)

        bin_string = b"".join(bin_list)
        wav_file.writeframes(bin_string)

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


if __name__ == "__main__":
    # Download from YouTube
    # get_youtube('https://www.youtube.com/watch?v=HCjNJDNzw8Y')

    # Load song
    y, sr = load("../../samples/dance_demo.mp3")
