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
        self.wfile.write(bytes(r"""{"thisPage": 2, "Cards": [{"Title": "Oregon Republicans are still on the lam to avoid voting on a major climate change bill", "Score": 5, "Date": "06/21/19", "Publisher": "Unknown", "Author": "Jun", "URL": "https://www.vox.com/2019/6/21/18700741/oregon-republican-walkout-climate-change-bill"}, {"Title": "test1", "Score": 5, "Date": "test2", "Publisher": "test4", "Author": "test3", "URL": "www.google.com"}]}""", "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))