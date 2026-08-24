#!/usr/bin/python3

import UGV02

ugv02 = UGV02.UGV02()
response = ugv02.write("{\"T\":1,\"L\": 0.2, \"R\": 0.2}\r\n")
if response == None:
    response = "No response from UGV"
print("UGV status: \n" + response)
