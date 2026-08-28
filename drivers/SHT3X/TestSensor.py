#!/usr/bin/python3

import SHT3X

status = SHT3X.SHT3X().get_measurements()
print("Sensor status: " + status)
