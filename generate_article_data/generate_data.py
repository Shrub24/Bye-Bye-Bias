import sys
import os
sys.path.append(os.getcwd())

from preprocessing.article_entities import *
from populate_database import *
import newspaper
import random
import pickle
from generate_article_data.load_articles import load_articles

if __name__ == "__main__":
    # generating sentences
    NUM_MAIN_ENTITIES = 5
    texts = load_articles("articles\\texts.pkl")
    sentences = list()
    for text in texts:
        text_entity_getter_instance = text_entity_getter(text)
        for entity in text_entity_getter_instance.get_n_important_entities(NUM_MAIN_ENTITIES):
            sentences += text_entity_getter_instance.get_sentence_target_tuples(entity)

    SOURCE_PATH = "sentences.pkl"
    source = open(SOURCE_PATH, "wb")
    pkl.dump(sentences, SOURCE_PATH)

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
    #
    # PICKLE_PATH = "generate_article_data/article_data.pkl"
    # if os.path.isfile(PICKLE_PATH):
    #     pickled_data = pickle.load(open(PICKLE_PATH, "rb"))
    #     pickle.dump(pickled_data + labelled_sentences, open(PICKLE_PATH, "wb"))
    # else:
    #     pickle.dump(labelled_sentences, open(PICKLE_PATH, "wb"))
