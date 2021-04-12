#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dancebots.utils as utils


audio, sample_rate = utils.load("../samples/motor_test.wav")
# audio, sample_rate = utils.load("./test_move.wav")
utils.plot(channel_l=audio[0], channel_r=audio[1], sample_rate=sample_rate)
