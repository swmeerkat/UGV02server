#!/usr/bin/python3

import UGV02

ugv02 = UGV02.UGV02()
response = ugv02.write("{\"T\":130}\r\n")
if response is None:
    response = "No response from UGV"
print("UGV status: \n" + response)