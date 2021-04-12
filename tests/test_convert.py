#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots.utils as utils
from dancebots import Move

move = Move()
move.forward(2)
move.backward(2)

beat_times = list(range(1, 5))


# 1. Moves only
bitstream = utils.convert.steps_to_bitstream(move.steps)
# utils.plot(bitstream)

# 2. Synchronize moves to beat times
bitstream = utils.convert.steps_to_bitstream(move.steps, beat_times)
# utils.plot(bitstream, xlim=[1, 1.05])

# 3. Beats bitstream
bitstream = utils.convert.beats_to_bitstream(beat_times)
# utils.plot(bitstream)
