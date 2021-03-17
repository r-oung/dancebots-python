#!/usr/bin/env python

"""
db_protocol.py: Builds dancebot file
"""

# __author__ = "Raymond Oung"
# __email__ = "raymond.oung@gmail.com"


# from __future__ import unicode_literals
from pydub import AudioSegment  # Python 2.7.x
from scipy.io import wavfile

import youtube_dl as yt
import numpy as np
import matplotlib.pyplot as plt


def get_youtube_mp3(html):
    # try:
    #     os.remove("*.mp3")
    # except OSError:
    #     pass

    print ("Downloading", html, "as MP3 from YouTube...")
    ytdl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download(["https://www.youtube.com/watch?v=HCjNJDNzw8Y"])

    return


def main():
    """
    INPUT
            arg0: song file (.WAV)
            arg1: dancebot choreography file (.WAV)

    OUTPUT
            Song file (.MP3) that contains both the song and choreography for dancebot use;
            Channel-1 (Left): song (mono)
            Channel-2 (Right): choreography
    """

    # print("Convert MP3 to WAV")
    # sound = AudioSegment.from_mp3("test.mp3")
    # sound.export("test.wav", format="wav")

    # import WAV file for manipulation
    rate, data = wavfile.read("test.wav")
    s = aubio.source("test.wav")
    print s.samplerate

    print ("No. Channels: {}".format(data.shape[1]))
    print ("No. Samples: {}".format(data.shape[0]))
    print ("Sampling Rate: {} Hz".format(rate))

    # ch_l = data[:,0] # left channel
    # ch_r = data[:,1] # right channel (motor)

    # manipulate channel-1 of wavefile
    # sindata = np.sin(data)
    # scaled = np.round(32767*sindata)
    # newdata = scaled.astype(np.int16)

    # ctrl = data.copy()
    # val = data.max()

    # for i in range(len(data)):
    # 	ctrl[i][0] = val

    # plt.subplot(211)
    # plt.plot(ctrl[:,0])
    # plt.xlabel('Sample')
    # plt.ylabel('Music Channel WAV')

    # plt.subplot(212)
    # plt.plot(ctrl[:,1])
    # plt.xlabel('Sample')
    # plt.ylabel('Control Channel WAV')

    # plt.show()

    # print("Export to WAV file")
    # wavfile.write('ctrl.wav', rate, ctrl)

    # print("Convert WAV to MP3")
    # sound = AudioSegment.from_wav("ctrl.wav")
    # sound.export("ctrl.mp3", format="mp3")


if __name__ == "__main__":
    main()
