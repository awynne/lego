#!/usr/bin/python

# 
# Uses package: python-rpi.gpio python3-rpi.gpio
# Library usage: http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# Tutorial: http://www.thirdeyevis.com/pi-page-2.php
#

import RPi.GPIO as gpio
import time

CHAN = 11 #7

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

assert gpio.getmode() == gpio.BOARD
gpio.setup(CHAN, gpio.OUT)

while True:
    gpio.output(CHAN, True)
    time.sleep(.4)
    gpio.output(CHAN, False)
    time.sleep(.4)



