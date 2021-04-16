# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116, R0201
import unittest
import dancebots.utils as utils
from dancebots.core import Step


class TestUtils(unittest.TestCase):
    def test_convert_beats_bitstream(self):
        beat_times = list(range(1, 5))
        utils.convert.beats_to_bitstream(beat_times)

    def test_convert_steps_to_bitstream(self):
        step = Step([1] * 8, [1] * 8, [1] * 8, 5)
        beat_times = list(range(1, 5))
        steps = [step] * 5

        # 1. Moves only
        utils.convert.steps_to_bitstream(steps)

        # 2. Synchronize moves to beat times
        utils.convert.steps_to_bitstream(steps, beat_times)


if __name__ == "__main__":
    unittest.main()
