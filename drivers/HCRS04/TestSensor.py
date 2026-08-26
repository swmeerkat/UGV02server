#!/usr/bin/env python3

import HCSR04

sensor = HCSR04.HCSR04()
distance_cm = sensor.getDistance()
print("Sensor status: distance= " + f"{distance_cm}" + "cm")
