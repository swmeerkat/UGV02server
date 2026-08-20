#!/usr/bin/python3

import time

import smbus

# # I2C bus = 7, default sensor address = 0x44
SENSOR_ADDRESS = 0x44
bus = smbus.SMBus(7)

# Clear status register
bus.write_byte_data(SENSOR_ADDRESS, 0x30, 0x41)
time.sleep(0.05)
#data1 = bus.read_i2c_block_data(SENSOR_ADDRESS, 0x00, 2)
#print("Status: 0x{:04x}".format((data1[0] << 8) + data1[1]))

# Write the sensor command
bus.write_byte_data(SENSOR_ADDRESS, 0x24, 0x00)
# Time to measure and save the data
time.sleep(0.05)

# Read data, 6 bytes
data = bus.read_i2c_block_data(SENSOR_ADDRESS, 0x00, 6)
t_msb = data[0]  # temp MSB
t_lsb = data[1]  # temp LSB
t_crc = data[2]  # temp check sum, ignored
h_msb = data[3]  # hum MSB
h_lsb = data[4]  # hum LSB
h_crc = data[5]  # hum check sum, ignored

# Convert temperature
t_val = (t_msb << 8) + t_lsb
T = ((175 * t_val) / 65535) - 45 # formula from data sheet

# Convert humidity
h_val = (h_msb << 8) + h_lsb
H = ((100 * h_val) / 65535) # formula from data sheet

print ("Temperature: {:.2f}".format(T))
print ("Humidity: {:.2f}".format(H))

# Read status register
bus.write_byte_data(SENSOR_ADDRESS, 0xF3, 0x2D)
time.sleep(0.05)
data1 = bus.read_i2c_block_data(SENSOR_ADDRESS, 0x00, 2)
print("Status: 0x{:04x}".format((data1[0] << 8) + data1[1]))

