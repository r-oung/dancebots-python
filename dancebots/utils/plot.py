#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt

def plot(y, sr):
    if len(y.shape) != 2:
        raise ValueError("Incorrect array shape")

    ch_l = y[0]
    ch_r = y[1]

    t = []
    for x in range(y.shape[1]):
        t.append(x / float(sr)) # [sec]

    # Plot bitstream
    ax1 = plt.subplot(211)
    plt.plot(t, ch_l)
    plt.ylabel('Left Channel')

    ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
    plt.plot(t, ch_r)
    plt.ylabel('Right Channel')
    plt.xlabel('Seconds')

    plt.show()


if __name__ == "__main__":
    from inout import load

    y, sr = load('../../samples/dance_demo.mp3')
    plot(y, sr)

# @TODO For any arbitrary input, show the start of a frame, left/right motor, and LEDs
# Guide: https://matplotlib.org/stable/tutorials/index.html
# Annotations: https://matplotlib.org/stable/tutorials/text/annotations.html#sphx-glr-tutorials-text-annotations-py