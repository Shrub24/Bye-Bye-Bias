from news_sentiment.doc_sentiment_analysis import *
from news_sentiment.cnn import *
from populate_database import *
from preprocessing.article_entities import *
from news_sentiment.data_prep import *
import numpy as np
import random
import collections
import mysql


if __name__ == "__main__":
    DB = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")
    net = load_model("models\\cnnyeet4.pkl")
    embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
    URL_PATH = "urls.txt"
    NUM_MAIN_ENTITIES = 3
    with open(URL_PATH, "r") as url_file:
        url_list = url_file.readlines()
    raw_infos = get_scraped_infos(url_list)
    raw_texts = [info["text"] for info in raw_infos]
    entity_sentiments = list()
    all_entities = list()
    for text in raw_texts:
        text_entity_getter_instance = text_entity_getter(text)
        entity_sentiments.append({entity_string: get_doc_sentiment(text_entity_getter_instance.get_sentence_target_tuples_from_tokens(sentence_target_tuple_input), net, embedding) for entity_string, sentence_target_tuple_input in text_entity_getter_instance.get_n_important_entities(NUM_MAIN_ENTITIES)})
        all_entities.append(text_entity_getter_instance.get_unique_relevant_entities_stripped())
    populate_database(generate_article_infos(raw_infos, entity_sentiments, all_entities), DB)