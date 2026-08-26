#!/usr/bin/env python3

import time

import Jetson.GPIO as GPIO

# trigger pin: pin 7 of expansion header
TRIGGER_PIN = 7
# echo pin: pin 15 of expansion header
ECHO_PIN = 15


class HCSR04:

    def __init__(self):
        # suppress "Could not open /dev/mem for pinmux check"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
        time.sleep(0.001)

    def getDistance(selfself):
        start = 0
        end = 0
        # send the trigger signal
        GPIO.output(TRIGGER_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIGGER_PIN, GPIO.LOW)
        # wait for the echo
        while GPIO.input(ECHO_PIN) == 0:
            start = time.perf_counter_ns()
        while GPIO.input(ECHO_PIN) == 1:
            end = time.perf_counter_ns()
        # elapsed time in s
        elapsed_time_s = (end - start) / 1000000000
        # speed of sound in the air: appr. 343.5 m/s at 20 °C -> 34350 cm/s
        # elapsed time is 2 times the distance to the object
        # distance = elapsed time * speed of sound / 2
        distance_cm = round(elapsed_time_s * 17175, 1)
        return distance_cm
        return distance_cm

    def __exit__(self, exception_type, exception_value, exception_traceback):
        GPIO.cleanup()
