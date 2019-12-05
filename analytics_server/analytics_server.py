import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from urllib.parse import parse_qs
from datetime import date
import json
import statistics

PORT_NUMBER = 8040


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        print(query)
        id = parse_qs(query)["id"][0]
        entity = parse_qs(query)["entity"][0]

        response = self.get_response(id, entity)

        print(response)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

        return

    def get_response(self, id, entity):
        t_name = "u" + id
        cur = analytics_db.cursor()
        cur.execute("SELECT DISTINCT main_entity FROM " + t_name)
        result = cur.fetchall()
        if result:
            all_entities = [i[0] for i in result]
        else:
            all_entities = []
        if not entity == "NULL":
            # get strength and interest data for past year
            current_date = date.today().toordinal()
            NUM_RETURNED_DATES = 365
            strength_history = []
            interest_history = []
            for i in range(0, NUM_RETURNED_DATES):
                i_date = current_date - (NUM_RETURNED_DATES - 1) + i
                cur.execute("SELECT strength FROM " + t_name + " WHERE main_entity = '" + entity + "' AND date = " + str(i_date) + ";")
                result = cur.fetchall()
                if result:
                    result_val = [i[0] for i in result]
                    # interest
                    interest_history.append(len(result_val))
                    # sentiment
                    strength_history.append(statistics.mean(result_val))
                else:
                    interest_history.append(0)
                    strength_history.append(5)
        else:
            strength_history = [0] * 365
            interest_history = [0] * 365


        return {"entities": all_entities, "sentiment": strength_history, "interest": interest_history}

        # {entities, strength history, interest history}


if __name__ == "__main__":
    analytics_db = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="analytics")

    server = HTTPServer(("", PORT_NUMBER), Handler)
    print("Startd httpserver on port " + str(PORT_NUMBER))
    server.serve_forever()