import sys
import os
sys.path.append(os.getcwd())

from preprocessing.article_entities import *
from populate_database import *
import newspaper
import random
import pickle

if __name__ == "__main__":
    # # add cnn fox news and more
    # PUBLISHER_LIST = ["https://edition.cnn.com/", "https://www.nbcnews.com/", "https://www.foxnews.com/"]
    # publisher = random.choice(PUBLISHER_LIST)
    # paper = newspaper.build(publisher)
    # for article in paper.articles:
    #     print(article.url)



    NUM_MAIN_ENTITIES = 5
    # url_list = [article.url for article in paper.articles]
    url_list = ["https://www.abc.net.au/news/2019-09-10/ricky-stuart-re-signed-to-raiders-canberra-nrl-coach/11493858?section=analysis"]
    raw_infos = get_scraped_infos(url_list)
    raw_texts = [info["text"] for info in raw_infos]
    raw_texts = raw_texts[:5]
    sentences = list()
    for text in raw_texts:
        text_entity_getter_instance = text_entity_getter(text)
        for entity in text_entity_getter_instance.get_n_important_entities(NUM_MAIN_ENTITIES):
            sentences += text_entity_getter_instance.get_sentence_target_tuples(entity)

    # any key to quit, n for bad sentence, -1 for neg, 0 for neut, 1 for pos
    labelled_sentences = list()
    for sentence, index in sentences:
        target = sentence[index[0]:index[1]]
        print(sentence[:index[0]] + "$T$" + sentence[index[1]:])
        print("target: " + target)
        label = input()
        if label in {"-1", "0", "1"}:
            labelled_sentences.append(((sentence, index), int(label)))
        elif label == "n":
            pass
        else:
            break

    PICKLE_PATH = "generate_article_data/article_data.pkl"
    if os.path.isfile(PICKLE_PATH):
        pickled_data = pickle.load(open(PICKLE_PATH, "rb"))
        pickle.dump(pickled_data + labelled_sentences, open(PICKLE_PATH, "wb"))
    else:
        pickle.dump(labelled_sentences, open(PICKLE_PATH, "wb"))
