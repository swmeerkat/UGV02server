#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time

trigger_pin = 7
echo_pin = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.output(trigger_pin, GPIO.LOW)
time.sleep(0.001)

start = 0
end = 0
# send the trigger signal
GPIO.output(trigger_pin, GPIO.HIGH)
time.sleep(0.00001)
GPIO.output(trigger_pin, GPIO.LOW)
# wait for the echo
while GPIO.input(echo_pin) == 0:
    start = time.perf_counter_ns()
while GPIO.input(echo_pin) == 1:
    end = time.perf_counter_ns()
# elapsed time in s
elapsed_time = (end - start) / 1000000000
# speed of sound: appr. 343 m/s at 20 °C -> 34300 cm/s
# elapsed time is 2 times the distance to the object
# distance = elapsed time * speed of sound / 2
distance = elapsed_time * 17150
print("distance: " + f"{distance}" + "cm")
GPIO.cleanup()