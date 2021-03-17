#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import wave
import struct


class Create:
    """
    Generate wavefile from audio samples
    """

    # Audio will contain a long list of samples (i.e. floating point numbers describing the
    # waveform).  If you were working with a very long sound you'd want to stream this to
    # disk instead of buffering it all in memory list this.  But most sounds will fit in
    # memory.

    def __init__(self, sample_rate=44100.0):
        self.audio_samples = []
        self.sample_rate = sample_rate

        return

    def get_samples(duration_milliseconds):
        return int(duration_milliseconds * (self.sample_rate / 1000.0))

    def append_silence(self, duration_milliseconds=500):
        """
        Adding silence is easy - we add zeros to the end of our array
        """
        num_samples = get_samples(duration_milliseconds)

        for x in range(num_samples):
            self.audio_samples.append(0.0)

        return

    def append_sinewave(freq=440.0, duration_milliseconds=500, volume=1.0):
        """
        The sine wave generated here is the standard beep.  If you want something
        more aggresive you could try a square or saw tooth waveform.   Though there
        are some rather complicated issues with making high quality square and
        sawtooth waves... which we won't address here :)
        """
        num_samples = get_samples(duration_milliseconds)

        for x in range(num_samples):
            self.audio_samples.append(
                volume * math.sin(2 * math.pi * freq * (x / self.sample_rate))
            )

        return

    def wav(self, file_name, audio_samples):
        # Open up a wav file
        wav_file = wave.open(file_name, "w")

        # wav params
        nchannels = 1
        sampwidth = 2

        # 44100 is the industry standard sample rate - CD quality.  If you need to
        # save on file size you can adjust it downwards. The stanard for low quality
        # is 8000 or 8kHz.
        nframes = len(audio)
        comptype = "NONE"
        compname = "not compressed"
        # https://docs.python.org/3/library/wave.html
        wav_file.setparams(
            (nchannels, sampwidth, sample_rate, nframes, comptype, compname)
        )

        # WAV files here are using short, 16 bit, signed integers for the
        # sample size.  So we multiply the floating point data we have by 32767, the
        # maximum value for a short integer.  NOTE: It is theortically possible to
        # use the floating point -1.0 to 1.0 data directly in a WAV file but not
        # obvious how to do that using the wave module in python.
        # https://soledadpenades.com/posts/2009/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
        for sample in audio_samples:
            wav_file.writeframes(struct.pack("h", int(sample * 32767.0)))

        wav_file.close()

        return


if __name__ == "__main__":
    create = Create()

    create.append_sinewave(volume=0.25)
    create.append_silence()
    create.append_sinewave(volume=0.5)
    create.append_silence()
    create.append_sinewave()

    # create.save_wav("output.wav")
