# -*- coding: utf-8 -*-
"""Bitstream object.

"""
from .frame import Frame


class Bitstream:
    """A class for converting a list of frames into a bitstream.

    Attributes:
        frames: A list of Frame objects.
        sample_rate: Audio sampling-rate (Hz)
    """

    # Static variables
    _DELIMITER = 2.0  # delimiter bit duration [msec]
    _ONE = 0.6  # one bit duration [msec]
    _ZERO = 0.2  # zero bit duration [msec]

    def __init__(self, frames=None, sample_rate=44100):
        if frames is not None:
            for frame in frames:
                if not isinstance(frame, Frame):
                    raise TypeError("👎 Must be of type Frame")

            self._frames = frames
        else:
            self._frames = []

        if sample_rate <= 0 or not isinstance(sample_rate, int):
            raise ValueError("👎 Sample rate must be a positive integer")

        self._sample_rate = sample_rate
        self._last_value = 1
        self._bits = []

        self._convert_frames_to_bits(frames)

    def _append(self, duration):
        num_samples = int(duration * (self._sample_rate / 1000.0))
        self._last_value *= -1  # toggle value
        self._bits += [self._last_value] * num_samples

    def _convert_frames_to_bits(self, frames):
        if frames is None:
            return

        for frame in frames:
            self._append(self._DELIMITER)
            for bit in frame.data:
                if bit == 0:
                    self._append(self._ZERO)
                elif bit == 1:
                    self._append(self._ONE)
                else:
                    raise ValueError("👎 Frame must contain binary values, i.e. 0 or 1")

    def __len__(self):
        return len(self._bits)

    def __add__(self, other):
        if self._sample_rate != other.sample_rate:
            raise ValueError("👎 Sampling rates are different")

        new_frames = self._frames.copy()
        new_frames = new_frames + other.frames
        return self.__class__(new_frames, self._sample_rate)

    def __radd__(self, other):
        if other == 0:
            return self

        return self.__add__(other)

    def __iadd__(self, other):
        if self._sample_rate != other.sample_rate:
            raise ValueError("👎 Sampling rates are different")

        self._frames += other.frames
        self._convert_frames_to_bits(other.frames)
        return self

    def __str__(self):
        """Pretty print steps"""
        lines = []
        for frame in self._frames:
            lines.append(str(frame))
        return "\n".join(lines)

    def __repr__(self):
        return "{}({},{})".format(
            self.__class__.__name__, self._frames, self._sample_rate
        )

    @property
    def bits(self):
        """Bits getter"""
        return self._bits

    @property
    def frames(self):
        """List of Frames getter"""
        return self._frames

    @property
    def duration(self):
        """Duration of the current list of bits"""
        sample_period = 1.0 / self._sample_rate
        return len(self._bits) * sample_period  # [seconds]

    @property
    def sample_rate(self):
        """Sampling-rate getter"""
        return self._sample_rate

    def append_bits(self, bits):
        """Append bits"""
        self._bits += bits
