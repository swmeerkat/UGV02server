#!/usr/bin/python3
import time

import serial

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

print("UGV02 UART via Expansion Header test")
serial_port = serial.Serial(
    port=SERIAL_PORT,
    baudrate=BAUD_RATE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
print(f"Serial port {SERIAL_PORT} opened successfully")
time.sleep(1)

try:
    serial_port.write("{\"T\":1,\"L\": 0.2, \"R\": 0.2}\r\n".encode())
    while True:
        if serial_port.in_waiting > 0:
            data = serial_port.readline().strip().decode("utf-8")
            print(f"Received response: {data}")

except KeyboardInterrupt:
    print("Exiting program")

except Exception as exception_error:
    print("Exit program error: %s", exception_error)

finally:
    serial_port.close()
    print('Done!')
