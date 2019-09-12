import json
import os
import pickle as pkl


def load_articles(save_path):
    file = open(save_path, "rb")
    return pkl.load(file)


def load_new_articles(articles_path):
    article_texts = list()
    for source in os.listdir(articles_path):
        source_path = os.path.join(articles_path, source)
        for article in os.listdir(source_path):
            article_path = os.path.join(source_path, article)
            article_file = open(article_path, "r")
            article_dict = json.load(article_file)
            article_text = article_dict["text"]
            article_texts.append(article_text)
    return article_texts


def save_articles(texts, save_path):
    file = open(save_path, "wb")
    pkl.dump(texts, file)

