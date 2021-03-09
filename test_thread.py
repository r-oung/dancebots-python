#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import threading

print "Script started."

class MyProcessingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print "Processing file #",x,"started...",
        # do something time-cosnuming
        time.sleep(1)
        print " finished."

for x in range(100):
    task = MyProcessingThread()
    task.start()
    try:
        task.join()
    except KeyboardInterrupt:
        break

print "Bye"
print "x=",x

sys.exit()