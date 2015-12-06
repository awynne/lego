#!/usr/bin/python

from wedo import WeDo
import time
import sys
import RPi.GPIO as gpio
import thread

wd = WeDo()

dist_thresh = 25 # close gate when distance is lower than
sec_open = 1     # stay open this long after train passes
sec_move = .5    # how long to move gate motor
sec_read = .1    # wait between sensor reads
speed_down = 40  # motor speed going down
speed_up = -40   # motor speed going up
light_1 = 13     # channel for light #1
light_2 = 15     # channel for light #2

# States
ST_UP = "up"
ST_DOWN = "down"
ST_CLOSING = "closing"
ST_OPENING = "opening"

# globals
verbose = True
state = None
led_enabled = True

#############################################

def main():
    init_led()
    start_test()

    while True:
        wait_until_on()

        if wd.distance < dist_thresh:
            thread.start_new_thread(blink_alt, (light_1, light_2, .4) )
            down()
            train_pass()
            up()

        time.sleep(sec_read)

#############################################

def init_led():
    if led_enabled:
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(False)

        assert gpio.getmode() == gpio.BOARD
        gpio.setup(light_1, gpio.OUT)
        gpio.setup(light_2, gpio.OUT)

def led_on(chan, t_on):
    if led_enabled:
        gpio.output(chan, True)
        time.sleep(t_on)

def led_swap(chan1, chan2, t_delay):
    if led_enabled:
        gpio.output(chan1, True)
        gpio.output(chan2, False)
        time.sleep(t_delay)
        gpio.output(chan1, False)
        gpio.output(chan2, True)
        time.sleep(t_delay)

def led_off(chan, t_off):
    if led_enabled:
        gpio.output(chan, False)
        time.sleep(t_off)

def start_test():
    log("startup test...")
    t_wait = .5

    for i in range(2):
        led_on(light_1, 0)
        led_on(light_2, 0)
        down()
        time.sleep(t_wait)
        led_off(light_1, 0)
        led_off(light_2, 0)
        up()
        time.sleep(t_wait)

    for i in range(3):
        blink_both(light_1, light_2, t_wait/2)

    log("state: %s" % state)
    log("led enabled: %s" % led_enabled)
    assert state == ST_UP
    log("ready")

def wait_until_on():
    if wd.distance is None:
        log("distance sensor is off")
        while wd.distance is None:
            time.sleep(sec_read)
        log("distance sensor is on")
        sys.stdout.flush()

def down():
    global state
    log("gate going down")
    state = ST_CLOSING
    sys.stdout.flush()
    wd.motor_a = speed_down
    time.sleep(sec_move)
    wd.motor_a = 0
    state = ST_DOWN

def blink_both(chan1, chan2, delay):
    led_on(chan1, 0)
    led_on(chan2, delay)
    led_off(chan1, 0)
    led_off(chan2, delay)

def blink_alt(chan1, chan2, delay):
    if led_enabled:
        while state == ST_DOWN or state == ST_CLOSING:
            gpio.output(chan1, True)
            gpio.output(chan2, False)
            time.sleep(.4)
            gpio.output(chan1, False)
            gpio.output(chan2, True)
            time.sleep(.4)
 
        gpio.output(chan1, False)
        gpio.output(chan2, False)

def blink(chan, delay):
    if led_enabled:
        while state == ST_CLOSING or state == ST_DOWN:
            led_on(chan, delay)
            led_off(chan, delay)

def train_pass():
    log("train passing")
    sys.stdout.flush()
    if wd.distance is not None:
        while wd.distance < dist_thresh:
            log_dist()
            time.sleep(sec_read)
    log_dist()
    log("train passed. waiting %d sec..." % sec_open)
    sys.stdout.flush()
    time.sleep(sec_open)

def up():
    global state
    log("gate going up")
    state = ST_OPENING
    wd.motor_a = speed_up
    time.sleep(sec_move)
    wd.motor_a = 0
    state = ST_UP

def log_dist():
    if wd.distance is not None:
        log("    distance: %d" % wd.distance)

def log(string):
    if verbose:
        print "%s" % string
        sys.stdout.flush()

#############################################

if __name__ == "__main__":
    main()

