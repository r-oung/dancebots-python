"""A complex dance composition.

"""
import random
import dancebots as db
from dancebots import Move, Light


def twist(repeat):
    move = Move()
    for _ in range(repeat):
        move.left(1)
        move.right(1)

    return move


def shuffle(repeat):
    move = Move()
    for _ in range(repeat):
        move.forward(1)
        move.backward(1)

    return move


def glitter(repeat, period=0.2):
    light = Light()
    for _ in range(repeat):
        leds = [random.randint(0, 1) for i in range(8)]
        light.hold(leds, period)
        light.hold([0] * 8, period)

    return light


def knightrider(repeat, period=0.2):
    light = Light()
    for i in range(repeat):
        leds = [1] + [0] * 7
        for j in range(8):
            leds = leds[-1:] + leds[:-1]
            light.hold(leds, period)
            light.hold([0] * 8, period)

    return light


def upUpDownDownLeftRightLeftRight(repeat):
    move = Move()
    for _ in range(repeat):
        move.forward(1)
        move.forward(1)
        move.backward(1)
        move.backward(1)
        move.left(1)
        move.right(1)
        move.left(1)
        move.right(1)

    return move


if __name__ == "__main__":
    # Basic moves
    spin_left = Move()
    spin_left.left(5)

    spin_right = Move()
    spin_right.right(5)

    # Basic lights
    blink = Light()
    blink.blink([1] * 8, 3, 10)

    hold = Light()
    hold.hold([1] * 8, 3)

    # Build audio file
    db.load("../data/sample.wav")  # load music file

    # Moves
    for _ in range(5):
        db.add(twist(4))
        db.add(spin_left)
        db.add(shuffle(4))
        db.add(spin_right)
        db.add(upUpDownDownLeftRightLeftRight(1))

    # Lights
    for _ in range(5):
        db.add(blink)
        db.add(glitter(5))
        db.add(knightrider(5))
        db.add(hold)

    db.save("dance_advance.wav")
