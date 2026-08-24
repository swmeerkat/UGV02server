#!/usr/bin/python3

import INA219

status = INA219.INA219().getPowerStatus()
print("UPS status: \n" + status)
