#!/usr/bin/python

# 
# Uses package: python-rpi.gpio python3-rpi.gpio
# Library usage: http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# Tutorial: http://www.thirdeyevis.com/pi-page-2.php
#

import RPi.GPIO as gpio
import time

CHAN1 = 13
CHAN2 = 15

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

assert gpio.getmode() == gpio.BOARD
gpio.setup(CHAN1, gpio.OUT)
gpio.setup(CHAN2, gpio.OUT)

while True:
    gpio.output(CHAN1, True)
    gpio.output(CHAN2, False)
    time.sleep(.4)
    gpio.output(CHAN1, False)
    gpio.output(CHAN2, True)
    time.sleep(.4)



