#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots import Move
from dancebots import Protocol


# Convert instructions / frames to audio
def convert_to_audio(moves, bpm=120):
  beat_length = 60 / bpm # seconds per beat

  protocol = Protocol()
  for move in moves:
    print(move)



if __name__ == "__main__":
  move = Move()

  move.forward(5)
  move.backward(5)
  move.left(5)
  move.right(5)
  move.stop(1)

  convert_to_audio(move.frames)
  # @TODO Check firmware to see if commands latch and/or there's a watchdog