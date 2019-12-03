
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import date
import json
import random
import math

PORT_NUMBER = 8080

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {"entities": ["trump", "putin", "biden", "kim jong un"], 
        "sentiment": [random.randint(0, 10) for i in range(0, 365)], 
        "interest": [random.randint(0, 10) for i in range(0, 365)]}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

        return

if __name__ == "__main__":
    server = HTTPServer(("", PORT_NUMBER), Handler)
    print("Startd httpserver on port " + str(PORT_NUMBER))
    server.serve_forever()