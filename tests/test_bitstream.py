# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116
import unittest
from dancebots.core import Frame, Bitstream


class TestBitstream(unittest.TestCase):
    def setUp(self):
        motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
        motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
        leds = [1, 0, 1, 0, 1, 0, 1, 0]
        self.frame1 = Frame(motor_l, motor_r, leds)

        motor_l = [0, 0, 0, 0, 1, 1, 1, 1]
        motor_r = [0, 0, 1, 1, 0, 0, 1, 1]
        leds = [0, 1, 0, 1, 0, 1, 0, 1]
        self.frame2 = Frame(motor_l, motor_r, leds)

    def test_init(self):
        Bitstream()
        Bitstream([self.frame1])
        Bitstream([self.frame1, self.frame2])

        with self.assertRaises(ValueError):
            Bitstream([self.frame1], -1)

        with self.assertRaises(ValueError):
            Bitstream([self.frame1], 0)

        with self.assertRaises(ValueError):
            Bitstream([self.frame1], 1.0)

    def test_add(self):
        bitstream1 = Bitstream([self.frame1])
        bitstream2 = Bitstream([self.frame2])
        bitstream1 + bitstream2

    def test_radd(self):
        bitstream1 = Bitstream([self.frame1])
        bitstream2 = Bitstream([self.frame2])
        bitstream2 + bitstream1

    def test_iadd(self):
        total = Bitstream([self.frame1])
        total += Bitstream([self.frame2])

    def test_len(self):
        bitstream1 = Bitstream([self.frame1])
        bitstream2 = Bitstream([self.frame1])
        total = bitstream1 + bitstream2

        self.assertEqual(len(bitstream1), 416)
        self.assertEqual(len(bitstream2), 416)
        self.assertEqual(len(total), 832)

    def test_properties(self):
        bitstream = Bitstream([self.frame1])
        self.assertEqual(len(bitstream.bits), 416)
        self.assertListEqual(bitstream.frames, [self.frame1])
        self.assertEqual(bitstream.sample_rate, 44100)

        bitstream = Bitstream([self.frame1, self.frame2], 48000)
        self.assertEqual(len(bitstream.bits), 912)
        self.assertListEqual(bitstream.frames, [self.frame1, self.frame2])
        self.assertEqual(bitstream.sample_rate, 48000)

    def test_print(self):
        bitstream = Bitstream([self.frame1])
        print(bitstream)


if __name__ == "__main__":
    unittest.main()
