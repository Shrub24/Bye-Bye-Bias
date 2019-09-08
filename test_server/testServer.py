from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
hostPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(r"""{"thisPage": 2, "Cards": [{"Title": "test1", "Score": 2, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 2, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 2, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 5, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 5, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 5, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 9, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"},{"Title": "test1", "Score": 9, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"}]}""", "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))