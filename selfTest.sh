#!/usr/bin/env bash

printf "Starting self test\n\n"
./drivers/SHT3X/TestSensor.py
printf "\n"
./drivers/UPSModuleC/TestUPSModule.py
printf "\n"
./drivers/UGV02/TestUgv02.py
printf "\n"
./drivers/HCRS04/TestSensor.py
printf "\nDone\n"
