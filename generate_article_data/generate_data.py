import sys
import os
sys.path.append(os.getcwd())

from preprocessing.article_entities import *
# from populate_database import *
import newspaper
import random
import pickle as pkl
from generate_article_data.load_articles import load_articles
import collections

if __name__ == "__main__":
    # generating sentences
    # NUM_MAIN_ENTITIES = 5
    # texts = set((i.replace('"', "")for i in load_articles("articles\\breitbart.pkl")))
    # sentences = list()
    # for i, text in enumerate(texts):
    #     if i % (len(texts)/10) == 0:
    #         print(i/len(texts))
    #     text_entity_getter_instance = text_entity_getter(text)
    #     for entity in text_entity_getter_instance.get_n_important_entities(NUM_MAIN_ENTITIES):
    #         sentence = text_entity_getter_instance.get_sentence_target_tuples_from_tokens(entity[1])
    #         sentences.extend(sentence)
    #
    # SOURCE_PATH = "test.pkl"
    # source = open(SOURCE_PATH, "wb")
    # pkl.dump(sentences, source)

    # any key to quit, n for bad sentence, 0 for neg, 1 for neut, 2 for pos
    # labelled_sentences = list()
    # sentence_generator = (sentence, index for sentence, index in sentences)
    # for sentence, index in sentence_generator:
    #     target = sentence[index[0]:index[1]]
    #     print(sentence[:index[0]] + "$T$" + sentence[index[1]:])
    #     print("target: " + target)
    #     label = input()
    #     if label in {"0", "1", "2"}:
    #         labelled_sentences.append(((sentence, index), int(label) - 1))
    #     elif label == "n":
    #         pass
    #     else:
    #         sentences = [(i, j) for i, j in sentence_generator]
    # source = open(SOURCE_PATH, "wb")
    # pkl.dump(sentences, SOURCE_PATH)

    dir_path = "generate_article_data/article_datas"
    data = list()
    for article_data_path in os.listdir(dir_path):
        article_data = pkl.load(open(os.path.join("generate_article_data/article_datas", article_data_path), "rb"))
        data.extend(article_data)
    data = [i for i in data if i[1] != 0 or random.randint(1, 3) == 1]
    data = [list(i) for i in zip(*data)]
    # pickle.load(open(PICKLE_PATH, "rb"))

    # if os.path.isfile(PICKLE_PATH):
    #     pickled_data = pickle.load(open(PICKLE_PATH, "rb"))
    #     pickle.dump(pickled_data + labelled_sentences, open(PICKLE_PATH, "wb"))
    # else:
    #     pickle.dump(labelled_sentences, open(PICKLE_PATH, "wb"))
