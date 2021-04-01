#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dancebots.core import Move, Light

def insert(obj):
  if isinstance(obj, Move):
    print("Move type")
  
  if isinstance(obj, Light):
    print("Light type")


move = Move()
move.forward(1)

light = Light()
light.hold([0,1,0,1,0,1,0,1], 1)

insert(move)
insert(light)
