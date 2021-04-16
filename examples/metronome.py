"""Create metronome test file.

"""
from dancebots import utils

# Load song file
audio, sample_rate = utils.load("../data/sample.wav")

# Get beats
bpm, beat_times = utils.get_beats(audio, sample_rate)
print("Number of beats: {}".format(len(beat_times)))
print("Estimated tempo: {:.2f} BPM".format(bpm))

# Construct metronome bitstream
bitstream = utils.convert.beats_to_bitstream(beat_times, sample_rate)

# Pad the bitstream so that it's the same length as the audio file
bitstream += [0] * (audio.shape[1] - len(bitstream))

# Build audio file
print("Building WAV file...")
utils.create_wav(
    channel_l=audio[0],
    channel_r=bitstream,
    filename="metronome.wav",
    sample_rate=sample_rate,
)
print("Done!")
