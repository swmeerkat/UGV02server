#!/usr/bin/env bash

printf "Starting self test\n\n"
./drivers/SHT3X/TestSensor.py
./drivers/UPSModuleC/TestUPSModule.py
./drivers/UGV02/TestUgv02.py
printf "\nDone\n"
