# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116, R0201
import unittest
import os
import dancebots as db
from dancebots import Move, Light

INPUT_WAV = "./data/sample.wav"
OUTPUT_WAV = "test.wav"


class TestDancebots(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(OUTPUT_WAV):
            os.remove(OUTPUT_WAV)
        else:
            print("File does not exist")

    def test_move_only(self):
        move = Move()
        move.clear()
        move.forward(3)
        move.backward(3)
        move.left(2)
        move.right(2)
        move.stop(1)

        db.add(move)
        db.save(OUTPUT_WAV)

    def test_light_only(self):
        light = Light()
        light.clear()
        light.blink([0, 1, 0, 1, 0, 1, 0, 1], 5)
        light.blink([1, 0, 1, 0, 1, 0, 1, 0], 5)
        light.hold([1, 0, 1, 0, 1, 0, 1, 0], 2)
        light.stop(1)

        db.add(light)
        db.save(OUTPUT_WAV)

    def test_move_light(self):
        move = Move()
        for _ in range(5):
            move.left(1)
            move.right(1)

        light = Light()
        light.blink([0, 1, 0, 1, 0, 1, 0, 1], 5)
        light.blink([1, 0, 1, 0, 1, 0, 1, 0], 5)
        light.hold([1, 0, 1, 0, 1, 0, 1, 0], 2)

        db.load(INPUT_WAV)
        db.add(move)
        db.add(light)
        db.save(OUTPUT_WAV)
    
    def example_08(self):
        move = Move()
        for _ in range(10):
            move.left(2)
            move.right(2)

        light = Light()
        light.blink([1] * 8, 20, 4)
        light.hold([1] * 8, 2)
        light.hold([0] * 8, 1)
        light.hold([1] * 8, 2)

        db.load(INPUT_WAV)
        db.add(move)
        db.add(light)
        db.save(OUTPUT_WAV)


if __name__ == "__main__":
    unittest.main()
