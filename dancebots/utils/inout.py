#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa
import youtube_dl as yt

def load(filename):
    # Load audio file without any modifications
    # https://librosa.org/doc/latest/generated/librosa.load.html
    y, sr = librosa.load(filename, sr=None, mono=False)
    print('Sampling rate: {} Hz | Channels: {} | Samples: {}'.format(sr, y.shape[0], y.shape[1]))
    return y, sr

def get_youtube(url):
    options = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
    }

    with yt.YoutubeDL(options) as ytdl:
        print ("Downloading: {}".format(url))
        ytdl.download([url])

    return


if __name__ == "__main__":
    # Download from YouTube
    # get_youtube('https://www.youtube.com/watch?v=HCjNJDNzw8Y')

    # Load song
    y, sr = load("../../samples/dance_demo.mp3")
    