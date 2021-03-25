#!/usr/bin/env python
# -*- coding: utf-8 -*-
import librosa

from .waveform import sinewave

def get_beats(y, sr):
    # Convert to mono
    mono = librosa.to_mono(y)

    # Separate harmonics and percussives into two waveforms
    y_harm, y_perc = librosa.effects.hpss(mono)

    # Beat track on the percussive signal
    # bpm, beat_frames = librosa.beat.beat_track(y=y_perc, sr=sr)
    bpm, beat_frames = librosa.beat.beat_track(y=mono, sr=sr)

    # Convert the frame indices of beat events into timestamps
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    return bpm, beat_times

def metronome(y, sr, beat_times):
    # Construct bitstream
    bitstream = []
    beat_index = 0
    sample_index = 0
    tone = sinewave(1000, sr)
    while sample_index < y.shape[1]:
        if beat_index >= len(beat_times):
            # If there are no more beats, append zero
            bitstream.append(0)
            sample_index += 1
        else:
            if sample_index / float(sr) < beat_times[beat_index]:
                # Off beat
                bitstream.append(0)
                sample_index += 1
            else:
                # On beat
                bitstream += tone
                sample_index += len(tone)
                beat_index += 1
    
    return bitstream


if __name__ == "__main__":
    from inout import load
    from convert import bitstream_to_wav

    # Load song file
    y, sr = load('../../samples/dance_demo.mp3')

    # Get beats
    bpm, beat_times = get_beats(y, sr)
    print('Number of beats: {}'.format(len(beat_times)))
    print('Estimated tempo: {:.2f} BPM'.format(bpm))

    # Construct metronome bitstream
    bitstream = metronome(y, sr, beat_times)

    # Construct WAV file
    print('Constructing WAV file...')
    bitstream_to_wav(ch_l=y[0], ch_r=bitstream, filename='output.wav')
    print('Done')
