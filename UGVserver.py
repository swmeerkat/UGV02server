#!/usr/bin/env python3

import json
import logging
import subprocess
from functools import cached_property
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

from drivers.HCRS04 import HCSR04
from drivers.OAKDS2 import OAKDS2
from drivers.SHT3X import SHT3X
from drivers.UGV02 import UGV02
from drivers.UPSModuleC import INA219


def gimbal_cam_on():
    command = "/home/jetson/UGV02server/scripts/start_gimbal_cam.sh"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process.stdout.decode("utf-8").strip()


def gimbal_cam_off(data):
    json_pid = json.loads(data)
    command = "kill -9 " + str(json_pid["gimbal_pid"])
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process.stdout.decode("utf-8").strip()


class UGVserver(BaseHTTPRequestHandler):

    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    def do_GET(self):
        content = "{}"
        status_code = 200
        match self.url.path:
            case "/ups/status":
                if ina219 is not None:
                    content = ina219.get_power_status()
            case "/env/status":
                if sht3x is not None:
                   content = sht3x.get_measurements()
            case "/rear/distance":
                if hcrs04 is not None:
                    content = hcrs04.get_distance()
            case _:
                content = "{ \"error\": \"unknown command: " + self.url.path + "\"}"
        # suppress http server logging
        self.send_response_only(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))
        logging.info("UGVserver GET response: " + content)

    def do_POST(self):
        content = "{}"
        status_code = 200
        match self.url.path:
            case "/ugv02/cmd":
                if ugv02 is not None:
                  response = ugv02.write(self.post_data.decode("utf-8") + "\n")
                  if content != "null":
                    content = str(response)
            case "/gimbal/camera/on":
                pid = gimbal_cam_on()
                content = "{ \"gimbal_pid\": \"" + str(pid) + "\"}"
            case "/gimbal/camera/off":
                result = gimbal_cam_off(self.post_data.decode("utf-8"))
                content = "{ \"result\": \"" + str(result) + "\" }"
            case _:
                content = "{ \"error\": \"unknown command: " + self.path + "\"}"
        # suppress http server logging
        self.send_response_only(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))
        logging.info("UGVserver POST response: " + content)


if __name__ == "__main__":
    print("Starting UGVserver")
    ugvServer = None
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)
    try:
        ugv02 = UGV02.UGV02()
    except:
        ugv02 = None
        print("--UGV02 chassis unavailable")
    oakds = OAKDS2.OAKDS2()
    try:
        ina219 = INA219.INA219()
    except:
        ina219 = None
        print("--Power sensor unavailable")
    try:
        sht3x = SHT3X.SHT3X()
    except:
        sht3x = None
        print("--Temperature/Humidity sensor unavailable")
    try:
        hcrs04 = HCSR04.HCSR04()
    except:
        hcrs04 = None
        print("--Rear distance sensor unavailable")
    try:
        ugvServer = HTTPServer(("0.0.0.0", 8000), UGVserver)
        print("++UGV server started at http://0.0.0.0:8000")
        ugvServer.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if ugvServer is not None:
            ugvServer.server_close()
        print("++UGV server stopped")
        exit(0)
