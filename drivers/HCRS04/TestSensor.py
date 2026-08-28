#!/usr/bin/env python3

import HCSR04

sensor = HCSR04.HCSR04()
distance_cm = sensor.get_distance()
print("Sensor status: distance= " + f"{distance_cm}" + "cm")
