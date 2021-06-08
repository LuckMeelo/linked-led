#!/usr/bin/env python3
##
# PROJECT, 2021
# test
# File description:
# test
##

import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


# Change this to your Raspberry Pi IP address (ip -4 address | grep inet)
host_name = '10.61.2.181'
# Port
host_port = 8000
state = "Off"


class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self, type):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def checkRequestedFiles(self, request_extension):
        if request_extension != ".py":
            f = open(self.path[1:]).read()
            self.do_HEAD("text/" + request_extension[1:])
            if (request_extension == ".html"):
                self.wfile.write(f.format(state, state).encode("utf-8"))
            else:
                self.wfile.write(bytes(f, 'utf-8'))
        else:
            f = "File not found"
            self.send_error(404, f)

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        if (self.path == "/"):
            self.path = '/index.html'
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            self.checkRequestedFiles(request_extension)
        except:
            f = "File not found"
            self.send_error(404, f)

    def do_POST(self):
        """ do_POST() can be tested using curl command
            'curl -d "submit=On" http://server-ip-address:port'
        """
        global state
        content_length = int(
            self.headers['Content-Length'])    # Get the size of data
        post_data = self.rfile.read(content_length).decode(
            "utf-8")   # Get the data
        try:
            post_data = post_data.split("=")[1]    # Only keep the value
        except:
            post_data = "Off"
        state = post_data
        # print(post_data)
        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18, GPIO.OUT)

        if post_data == 'On':
            GPIO.output(18, GPIO.HIGH)
        else:
            GPIO.output(18, GPIO.LOW)
        print("LED is {}".format(post_data))
        self._redirect('/')    # Redirect back to the root url

        print("LED is {}".format(post_data))
        self._redirect('/')    # Redirect back to the root url


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
