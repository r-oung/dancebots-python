# -*- coding: utf-8 -*-
# pylint: disable=C0114, C0115, C0116
import unittest
from dancebots.core import Move, Light, Compose


class TestCompose(unittest.TestCase):
    def setUp(self):
        self.move1 = Move()
        self.move1.forward(3)
        self.move1.backward(3)
        self.move1.stop(1)

        self.move2 = Move()
        self.move2.left(3)
        self.move2.right(3)
        self.move2.stop(1)

        self.light1 = Light()
        self.light1.blink([0, 1, 0, 1, 0, 1, 0, 1], 3, 4)
        self.light1.blink([1, 1, 0, 0, 1, 1, 0, 0], 3, 3)
        self.light1.stop(1)

        self.light2 = Light()
        self.light2.hold([1] * 8, 4)
        self.light2.blink([1, 0, 1, 0, 1, 0, 1, 0], 3, 5)

    def test_init(self):
        Compose(moves=[self.move1, self.move2])
        Compose(lights=[self.light1, self.light2])
        Compose(moves=[self.move1, self.move2], lights=[self.light1, self.light2])
        Compose(moves=[self.move1], lights=[self.light1, self.light2])
        Compose(moves=[self.move1, self.move2], lights=[self.light1])

    def test_properties(self):
        light = Light()
        light.blink([0, 1, 0, 1, 0, 1, 0, 1], 3, 1)
        composition = Compose(lights=[light])
        self.assertEqual(composition.steps[0].num_units, 1)

        light = Light()
        light.blink([0, 1, 0, 1, 0, 1, 0, 1], 3, 2)
        composition = Compose(lights=[light])
        self.assertEqual(composition.steps[0].num_units, 0.5)

        light = Light()
        light.blink([0, 1, 0, 1, 0, 1, 0, 1], 3, 4)
        composition = Compose(lights=[light])
        self.assertEqual(composition.steps[0].num_units, 0.25)

    def test_print(self):
        compose = Compose(
            moves=[self.move1, self.move2], lights=[self.light1, self.light2]
        )
        print(compose)


if __name__ == "__main__":
    unittest.main()
