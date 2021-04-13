# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116, R0201
import unittest
from dancebots.core import Light


class TestLight(unittest.TestCase):
    def test_init(self):
        Light()

    def test_methods(self):
        light = Light()
        light.clear()
        light.blink([1, 0, 1, 0, 1, 0, 1, 0], 3, 2)
        light.hold([1, 1, 0, 0, 1, 1, 0, 0], 2)
        light.stop(1)
        self.assertEqual(len(light.steps), 8)

    def test_arguments(self):
        light = Light()

        with self.assertRaises(ValueError):
            light.blink([0] * 9, 1, 1)

        with self.assertRaises(ValueError):
            light.blink([2] * 8, 1, 1)

        with self.assertRaises(ValueError):
            light.blink([1] * 8, -1, 1)

        with self.assertRaises(ValueError):
            light.blink([1] * 8, 0, 1)

        with self.assertRaises(ValueError):
            light.blink([1] * 8, 1.1, 1)

        with self.assertRaises(ValueError):
            light.blink([1] * 8, 1, -1)

        with self.assertRaises(ValueError):
            light.blink([1] * 8, 1, 0)

        with self.assertRaises(ValueError):
            light.blink([1] * 8, 1, 1.1)

    def test_print(self):
        light = Light()
        light.blink([1, 0, 1, 0, 1, 0, 1, 0], 3, 2)
        print(light)


if __name__ == "__main__":
    unittest.main()
