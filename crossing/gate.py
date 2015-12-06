#!/usr/bin/python

from wedo import WeDo
import time
import sys

wd = WeDo()

numargs = len(sys.argv)

if numargs < 2:
    print "ERROR: command (up or down) must be first arg"
    sys.exit(-1)

cmd = sys.argv[1]

if cmd == "up":
    wd.motor_a = -30
    time.sleep(.5)
    wd.motor_a = 0
elif cmd == "down":
    wd.motor_a = 30
    time.sleep(.5)
    wd.motor_a = 0
else:
    print "ERROR: don't know command: (%s)" % cmd
    exit(-1)

