#!/usr/bin/python

# 
# Uses package: python-rpi.gpio python3-rpi.gpio
# Library usage: http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# Tutorial: http://www.thirdeyevis.com/pi-page-2.php
#

import RPi.GPIO as gpio
import time
import sys

#CHAN = 13 #15

numargs = len(sys.argv)

if numargs < 2:
    print "ERROR: GPIO pin number must be first arg"
    sys.exit(-1)

chan = int( sys.argv[1] )

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

assert gpio.getmode() == gpio.BOARD
gpio.setup(chan, gpio.OUT)

while True:
    gpio.output(chan, True)
    time.sleep(.4)
    gpio.output(chan, False)
    time.sleep(.4)



