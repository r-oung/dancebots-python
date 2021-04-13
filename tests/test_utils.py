# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116, R0201
import unittest
import dancebots.utils as utils
from dancebots.core import Step


class TestUtils(unittest.TestCase):
    def test_convert(self):
        step = Step([0, 1] * 4, [1, 0] * 4, [0, 1] * 4, 5)
        beat_times = list(range(1, 10))

        steps = [step] * 5

        # 1. Moves only
        utils.convert.steps_to_bitstream(steps)

        # 2. Synchronize moves to beat times
        utils.convert.steps_to_bitstream(steps, beat_times)

        # 3. Beats bitstream
        utils.convert.beats_to_bitstream(beat_times)


if __name__ == "__main__":
    unittest.main()
