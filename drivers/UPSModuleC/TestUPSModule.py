#!/usr/bin/python3

import INA219

status = INA219.INA219().get_power_status()
print("UPS status: \n" + status)
