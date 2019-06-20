import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

PORT_NUMBER = 8000

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        print(query)
        # self.send_response(200)
        # self.wfile.write("hiii")
        return


def get_strength_and_similar(url):
    cur = db.cursor()
    cur.execute("SELECT strength, topic FROM articles WHERE url='" + url + "'")
    result = cur.fetchall()[0]
    strength = result[0]
    topic = result[1]
    cur.execute("SELECT url, strength FROM articles WHERE topic='" + topic + "'")
    return (topic, strength, cur.fetchall())

if __name__ == "__main__":
    db = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")

    server = HTTPServer(("", PORT_NUMBER), Handler)
    print("Startd httpserver on port " + str(PORT_NUMBER))
    server.serve_forever()
    # print(get_strength_and_similar("www.test.com"))
    # db.close()
