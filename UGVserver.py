#!/usr/bin/env python3

import json
import subprocess
from functools import cached_property
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

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
                content = ina219.get_power_status()
            case "/env/status":
                content = sht3x.get_measurements()
            case _:
                content = "{ \"error\": \"unknown command: " + self.url.path + "\"}"
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_POST(self):
        content = "{}"
        status_code = 200
        match self.url.path:
            case "/ugv02/cmd":
                response = ugv02.write(self.post_data.decode("utf-8") + "\n")
                if content != "null":
                    content = str(response)
                    print(content)
            case "/gimbal/camera/on":
                pid = gimbal_cam_on()
                content = "{ \"gimbal_pid\": \"" + str(pid) + "\"}"
            case "/gimbal/camera/off":
                result = gimbal_cam_off(self.post_data.decode("utf-8"))
                content = "{ \"result\": \"" + str(result) + "\" }"
            case _:
                content = "{ \"error\": \"unknown command: " + self.path + "\"}"
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


if __name__ == "__main__":
    ugvServer = None
    try:
        ugv02 = UGV02.UGV02()
        oakds = OAKDS2.OAKDS2()
        ina219 = INA219.INA219()
        sht3x = SHT3X.SHT3X()
        ugvServer = HTTPServer(("0.0.0.0", 8000), UGVserver)
        print("UGV server started at http://0.0.0.0:8000")
        ugvServer.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if ugvServer is not None:
            ugvServer.server_close()
        print("UGV server stopped")
        exit(0)
