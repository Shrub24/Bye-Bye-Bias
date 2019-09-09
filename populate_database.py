from newspaper import Article
# from news_sentiment import main
from preprocessing.article_entities import entity_getter
import json
import mysql.connector


def scrape_article(article_url):
    print(article_url.strip())
    article = Article(url=article_url.strip())
    article.download()
    article.parse()
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
def populate_database(article_infos):
    DB = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")
    # create database if does not exist
    cur = DB.cursor()
    cur.execute("SHOW TABLES LIKE 'articles'")
    result = cur.fetchone()
    if not result:
        cur.execute("CREATE TABLE articles (title VARCHAR(350), publish_date VARCHAR (100), authors VARCHAR(500), url VARCHAR(600), publisher VARCHAR(500), entities VARCHAR(4000), main_entities VARCHAR(1000))")

    KEYS_TO_STORE = ("title", "publish_date", "authors", "url", "publisher", "entities", "main_entities")
    for article_info in article_infos:
        add_to_database({key: article_info[key] for key in KEYS_TO_STORE}, DB, "articles")


def generate_article_infos(scraped_info, main_entity_sentiments, all_entities):
    PUBLISHER_PATH = "publishers.txt"

    # import PUBLISHER_DICT from text doc
    PUBLISHER_DICT = dict()
    with open(PUBLISHER_PATH) as publish_file:
        for line in publish_file:
            split = line.split(";")
            PUBLISHER_DICT[split[0]] = split[1].strip()

    # with open(URL_PATH, "r") as url_file:
    article_infos = list()
    for i, article_info_i in enumerate(scraped_info):

        # article_info = scrape_article(url.strip())
        article_info = dict(article_info_i)
        # todo get part of url pertaining to publisher
        url_publisher = article_info["url"].split("/")[2]
        if url_publisher in PUBLISHER_DICT:
            article_info["publisher"] = PUBLISHER_DICT[url_publisher]
        else:
            article_info["publisher"] = "Unknown"
        text = article_info["text"]
        # article_info["entities"] = json.dumps(enttity_getter_instance.get_unique_relevant_entities_stripped(text))
        article_info["entities"] = json.dumps(all_entities[i])
        # main_entities = dict()
        # for entity in enttity_getter_instance.get_n_important_entities(text, NUMBER_OF_MAIN_ENTITIES_STORED):
        #     # todo get sentiment from neural network
        #     sentiment = get_doc_sentiment(enttity_getter_instance.get_sentence_target_lists(text, entity))
        #     main_entities[entity] = sentiment
        article_info["main_entities"] = json.dumps(main_entity_sentiments[i])
        article_infos.append(article_info)
    return article_infos

def get_scraped_infos(url_list):
    return [scrape_article(url) for url in url_list]

def get_all_entities(text_list, entity_getter_instance):
    return [entity_getter_instance.get_unique_relevant_entities_stripped(text) for text in text_list]

# def get_main_entities(text_list, entity_getter_instance, num_main_entities):
#     return [entity_getter_instance.get_n_important_entities(text, num_main_entities) for text in text_list]

# populate_database()