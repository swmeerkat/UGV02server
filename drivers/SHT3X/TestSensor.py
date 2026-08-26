#!/usr/bin/python3

import SHT3X

status = SHT3X.SHT3X().getMeasurements()
print("Sensor status: " + status)
