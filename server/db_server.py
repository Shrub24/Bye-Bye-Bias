import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

PORT_NUMBER = 8000


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        print(query)
        # self.send_response(200)
        response = get_strength_and_similar(query)
        print(response)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())
        return


def get_strength_and_similar(url):
    cur = db.cursor()
    cur.execute("SELECT strength, topic FROM articles WHERE url='" + url + "'")
    query_result = cur.fetchall()
    if not query_result:
        return{"topic": "unknown", "strength": 0, "articles": {}}
    else:
        result = query_result[0]
        strength = result[0]
        topic = result[1]
        cur.execute("SELECT url, strength FROM articles WHERE topic='" + topic + "'")
        articles = cur.fetchall()
        return {"topic": topic, "strength": strength, "articles": {str(i[0]): i[1] for i in articles}}


if __name__ == "__main__":
    db = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")

    server = HTTPServer(("", PORT_NUMBER), Handler)
    print("Startd httpserver on port " + str(PORT_NUMBER))
    server.serve_forever()
    # print(get_strength_and_similar("www.test.com"))
    # db.close()
