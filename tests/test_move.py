# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116, R0201
import unittest
from dancebots.core import Move


class TestMove(unittest.TestCase):
    def test_init(self):
        Move()

    def test_methods(self):
        move = Move()
        move.clear()
        move.forward(3)
        move.backward(3)
        move.left(2)
        move.right(2)
        move.stop(1)
        self.assertEqual(len(move.steps), 5)

    def test_arguments(self):
        move = Move()

        with self.assertRaises(ValueError):
            move.forward(-1)

        with self.assertRaises(ValueError):
            move.forward(0)

        with self.assertRaises(ValueError):
            move.forward(1, -1)

        with self.assertRaises(ValueError):
            move.forward(1, 101)

    def test_conversion(self):
        move = Move()

        motor_l, motor_r = move.forward(1, 100)
        self.assertListEqual(motor_l, [0, 0, 1, 0, 0, 1, 1, 1])
        self.assertListEqual(motor_r, [0, 0, 1, 0, 0, 1, 1, 1])

        move.clear()
        motor_l, motor_r = move.forward(1, 50)
        self.assertListEqual(motor_l, [0, 1, 0, 0, 1, 1, 0, 1])
        self.assertListEqual(motor_r, [0, 1, 0, 0, 1, 1, 0, 1])

        move.clear()
        motor_l, motor_r = move.forward(1, 0)
        self.assertListEqual(motor_l, [0, 0, 0, 0, 0, 0, 0, 1])
        self.assertListEqual(motor_r, [0, 0, 0, 0, 0, 0, 0, 1])

        move.clear()
        motor_l, motor_r = move.backward(1, 100)
        self.assertListEqual(motor_l, [0, 0, 1, 0, 0, 1, 1, 0])
        self.assertListEqual(motor_r, [0, 0, 1, 0, 0, 1, 1, 0])

        move.clear()
        motor_l, motor_r = move.backward(1, 50)
        self.assertListEqual(motor_l, [0, 1, 0, 0, 1, 1, 0, 0])
        self.assertListEqual(motor_r, [0, 1, 0, 0, 1, 1, 0, 0])

        move.clear()
        motor_l, motor_r = move.backward(1, 0)
        self.assertListEqual(motor_l, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertListEqual(motor_r, [0, 0, 0, 0, 0, 0, 0, 0])

        move.clear()
        motor_l, motor_r = move.left(1, 100)
        self.assertListEqual(motor_l, [0, 0, 1, 0, 0, 1, 1, 0])
        self.assertListEqual(motor_r, [0, 0, 1, 0, 0, 1, 1, 1])

        move.clear()
        motor_l, motor_r = move.left(1, 50)
        self.assertListEqual(motor_l, [0, 1, 0, 0, 1, 1, 0, 0])
        self.assertListEqual(motor_r, [0, 1, 0, 0, 1, 1, 0, 1])

        move.clear()
        motor_l, motor_r = move.left(1, 0)
        self.assertListEqual(motor_l, [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertListEqual(motor_r, [0, 0, 0, 0, 0, 0, 0, 1])

        move.clear()
        motor_l, motor_r = move.right(1, 100)
        self.assertListEqual(motor_l, [0, 0, 1, 0, 0, 1, 1, 1])
        self.assertListEqual(motor_r, [0, 0, 1, 0, 0, 1, 1, 0])

        move.clear()
        motor_l, motor_r = move.right(1, 50)
        self.assertListEqual(motor_l, [0, 1, 0, 0, 1, 1, 0, 1])
        self.assertListEqual(motor_r, [0, 1, 0, 0, 1, 1, 0, 0])

        move.clear()
        motor_l, motor_r = move.right(1, 0)
        self.assertListEqual(motor_l, [0, 0, 0, 0, 0, 0, 0, 1])
        self.assertListEqual(motor_r, [0, 0, 0, 0, 0, 0, 0, 0])

    def test_print(self):
        move = Move()
        move.forward(3)
        move.backward(3)
        print(move)


if __name__ == "__main__":
    unittest.main()
