#!/usr/bin/env python3
import logging
import time

import serial

_SERIAL_PORT = "/dev/ttyUSB0"
_BAUD_RATE = 115200


class UGV02:

    def __init__(self):
        self.serial_port = serial.Serial(
            port=_SERIAL_PORT,
            baudrate=_BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        time.sleep(1)
        print("UGV02 driver initialized")

    def read(self):
        try:
            self.serial_port.reset_input_buffer()
            response = ' '
            while response[0] != "{":
                response = self.serial_port.readline().strip().decode("utf-8")
            return response
        except Exception as exception_error:
            logging.error("ESP32 communication error: " + str(exception_error))
        finally:
            pass

    def write(self, data):
        response = {}
        try:
            self.serial_port.write(bytes(data + "\n", "utf-8"))
            while True:
                if self.serial_port.in_waiting > 0:
                    # ESP32 controller mirrors the command
                    response = self.serial_port.readline().strip().decode("utf-8")
                    break
            while True:
                if self.serial_port.in_waiting > 0:
                    response = self.serial_port.readline().strip().decode("utf-8")
                    logging.info(f"Received response: {response}")
                return response
        except Exception as exception_error:
            logging.error("ESP32 communication error: " + str(exception_error))
        finally:
            pass

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.serial_port.flush()
        self.serial_port.reset_input_buffer()
        self.serial_port.reset_output_buffer()
        self.serial_port.close()
