from doc_sentiment_analysis import *
from news_sentiment.tdbert import *
from populate_database import *
from preprocessing.article_entities import *
from news_sentiment.data_prep import *
import numpy as np
import random
import collections
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import mysql


def get_doc_sent(sentences):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    sentiments = list()
    for sentence in sentences:
        sents = sentiment_analyzer.polarity_scores(sentence[0])
        sents['compound'] = 0
        if sents["neg"] > sents["pos"]:
            sentiments.append(max(-1 * sents["neg"] * 4, -1))
        elif sents["neg"] < sents["pos"]:
            sentiments.append(min(sents["pos"] * 4, 1))
        else:
            sentiments.append(0)

    return (np.average(sentiments) + 1) * 4.5 + 1


if __name__ == "__main__":
    DB = mysql.connector.connect(host="localhost", user="root", passwd="bias123", db="articles")
    net = load_model("models\\bert2.pkl")
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
        entity_sentiments.append({entity: get_doc_sentiment(text_entity_getter_instance.get_sentence_target_tuples(entity), net) for entity in text_entity_getter_instance.get_n_important_entities(NUM_MAIN_ENTITIES)})
        all_entities.append(text_entity_getter_instance.get_unique_relevant_entities_stripped())
    populate_database(generate_article_infos(raw_infos, entity_sentiments, all_entities), DB)
