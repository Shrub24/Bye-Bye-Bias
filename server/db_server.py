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
        response = self.get_response(query)
        print(response)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())
        return


    def get_response(self, url):
        NUMBER_OF_RETURNED_ARTICLES = 30
        cur = db.cursor()
        cur.execute("SELECT entities, main_entities, title, publish_date, authors, publisher FROM articles WHERE url='" + url + "'")
        query_result = cur.fetchall()
        if not query_result:
            return {"title": "unknown", "strength": 0, "articles": [], "publish_date": "unknown", "publisher": "unknown", "authors": "unknown"}
        else:
            result = query_result[0]
            entities, main_entities, title, publish_date, authors, publisher = result
            entities = json.loads(entities)
            main_entities = json.loads(main_entities)
            main_entity = list(main_entities.keys())[0]
            strength = list(main_entities.values())[0]
            print(main_entity)
            cur.execute("SELECT entities, main_entities, title, publish_date, authors, publisher, url FROM articles WHERE main_entities LIKE '%\"" + main_entity + "\":%' AND url!='" + url + "'")
            query_result = cur.fetchall()
            other_articles = dict()
            other_articles_similarity = dict()
            for result in query_result:
                similar_entities, similar_main_entities, similar_title, similar_publish_date, similar_authors, similar_publisher, similar_url = result
                similar_entities = json.loads(similar_entities)
                similar_main_entities = json.loads(similar_main_entities)
                other_articles[similar_url] = {"title": similar_title, "strength": similar_main_entities[main_entity], "publish_date": similar_publish_date, "publisher": similar_publisher, "authors": similar_authors, "url": similar_url}
                other_articles_similarity[similar_url] = self.get_similarity_value(entities, similar_entities)
            similar_urls = sorted(list(other_articles_similarity.keys()), key=lambda x: other_articles_similarity[x], reverse=True)[:NUMBER_OF_RETURNED_ARTICLES]

            return {"title": title, "strength": strength, "articles": [other_articles[url] for url in similar_urls], "publish_date": publish_date, "publisher": publisher, "authors": authors}

    def get_similarity_value(self, entities_a, entities_b):
        similar = len(set(entities_a).intersection(entities_b))
        unique = len(entities_a) + len(entities_b) - (2 * similar)
        return similar/(similar + unique)


if __name__ == "__main__":
    db = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")

    server = HTTPServer(("", PORT_NUMBER), Handler)
    print("Startd httpserver on port " + str(PORT_NUMBER))
    server.serve_forever()
    # print(get_strength_and_similar("www.test.com"))
    # db.close()
