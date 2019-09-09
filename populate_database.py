from newspaper import Article
from preprocessing.article_entities import entity_getter
# from news_sentiment import main
import json
import mysql.connector


def scrape_article(article_url):
    article = Article(url=article_url)
    article.download()
    article.parse()
    print(article_url)
    return {"title": article.title, "publish_date": article.publish_date.strftime("%x"), "authors": ", ".join(article.authors), "text": article.text, "url": article_url}


# adds entry to mysql database given by values of dict corresponding to column titles of dict keys
# no apostrophes allowed in keys
def add_to_database(dict, db, table):
    cur = db.cursor()
    insert_command = "INSERT INTO " + table + " (" + str(dict.keys())[11:-2].replace("'", "") + ") VALUES (" + str(dict.values())[13:-2] + ");"
    cur.execute(insert_command)
    db.commit()


# todo validate urls (check for errors when processing)
# todo add create database condition
if __name__ == "__main__":
    enttity_getter_instance = entity_getter()
    URL_PATH = "urls.txt"
    NUMBER_OF_MAIN_ENTITIES_STORED = 3
    KEYS_TO_STORE = ("title", "publish_date", "authors", "url", "publisher", "entities", "main_entities")
    DB = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")
    # create database if does not exist
    cur = DB.cursor()
    cur.execute("SHOW TABLES LIKE 'articles'")
    result = cur.fetchone()
    if not result:
        cur.execute("CREATE TABLE articles (title VARCHAR(350), publish_date VARCHAR (100), authors VARCHAR(500), url VARCHAR(600), publisher VARCHAR(500), entities VARCHAR(4000), main_entities VARCHAR(1000))")

    # todo import PUBLISHER_DICT from text doc
    PUBLISHER_DICT = dict()
    with open(URL_PATH, "r") as url_file:
        for url in url_file:
            article_info = scrape_article(url.strip())
            # todo get part of url pertaining to publisher
            url_publisher = url
            if url_publisher in PUBLISHER_DICT:
                article_info["publisher"] = PUBLISHER_DICT[url_publisher]
            else:
                article_info["publisher"] = "Unknown"
            text = article_info["text"]
            article_info["entities"] = json.dumps(enttity_getter_instance.get_unique_relevant_entities_stripped(text))
            main_entities = dict()
            for entity in enttity_getter_instance.get_n_important_entities(text, NUMBER_OF_MAIN_ENTITIES_STORED):
                # todo get sentiment from neural network
                sentiment = 1
                main_entities[entity] = sentiment
            article_info["main_entities"] = json.dumps(main_entities)
            add_to_database({key: article_info[key] for key in KEYS_TO_STORE}, DB, "articles")


