# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116
import unittest
from dancebots.core import Frame


class TestFrame(unittest.TestCase):
    def setUp(self):
        self.motor_l = [1, 1, 1, 1, 0, 0, 0, 0]
        self.motor_r = [1, 1, 0, 0, 1, 1, 0, 0]
        self.leds = [1, 0, 1, 0, 1, 0, 1, 0]

    def test_init(self):
        frame = Frame(self.motor_l, self.motor_r, self.leds)
        self.assertEqual(frame.data, self.motor_l + self.motor_r + self.leds)

        with self.assertRaises(ValueError):
            Frame([0] * 9, [0] * 8, [0] * 8)

        with self.assertRaises(ValueError):
            Frame([0] * 8, [0] * 9, [0] * 8)

        with self.assertRaises(ValueError):
            Frame([0] * 8, [0] * 8, [0] * 9)

        with self.assertRaises(ValueError):
            Frame([0] * 9, [0] * 9, [0] * 8)

        with self.assertRaises(ValueError):
            Frame([0] * 8, [0] * 9, [0] * 9)

        with self.assertRaises(ValueError):
            Frame([0] * 9, [0] * 9, [0] * 9)

        with self.assertRaises(ValueError):
            Frame([2] * 8, [0] * 8, [0] * 8)

        with self.assertRaises(ValueError):
            Frame([0] * 8, [2] * 8, [0] * 8)

        with self.assertRaises(ValueError):
            Frame([0] * 8, [0] * 8, [2] * 8)

    def test_methods(self):
        frame = Frame(self.motor_l, self.motor_r, self.leds)
        print(frame)


if __name__ == "__main__":
    unittest.main()
