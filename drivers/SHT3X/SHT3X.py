#!/usr/bin/env python3

import time

import smbus


class SHT3X:

    # I2C bus = 7, default address = 0x44
    def __init__(self, i2c_bus=7, addr=0x44):
        self.bus = smbus.SMBus(i2c_bus)
        self.addr = addr

        # Clear status register
        self.bus.write_byte_data(self.addr, 0x30, 0x41)
        time.sleep(0.015)

    def read_values(self):
        # Write the sensor command
        self.bus.write_byte_data(self.addr, 0x24, 0x00)

        # Time to measure and save the data
        time.sleep(0.015)

        # Read data, 6 bytes
        data = self.bus.read_i2c_block_data(self.addr, 0x00, 6)
        return data

    def getMeasurements(self):
        data = self.read_values()
        t_msb = data[0]  # temp MSB
        t_lsb = data[1]  # temp LSB
        h_msb = data[3]  # hum MSB
        h_lsb = data[4]  # hum LSB

        # Convert temperature
        t_hex = (t_msb << 8) + t_lsb
        t = ((175 * t_hex) / 65535) - 45  # formula from data sheet
        t_val = ("{:.2f}".format(t))

        # Convert humidity
        h_hex = (h_msb << 8) + h_lsb
        h = ((100 * h_hex) / 65535)  # formula from data sheet
        h_val = ("{:.2f}".format(h))

        return ("{\"temperature\": " + t_val + "," +
                "\"humidity\": " + h_val + "}")
