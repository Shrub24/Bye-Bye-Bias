from news_sentiment.doc_sentiment_analysis import *
from news_sentiment.cnn import *
# from populate_database import *
from preprocessing.article_entities import *
from news_sentiment.data_prep import *
import numpy as np
import random


if __name__ == "__main__":
    # DB = mysql.connector.connect(host="localhost", user="byebyebias", passwd="bias123", db="articles")
    # net = load_model("models\\cnn3.pkl")
    # embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
    # URL_PATH = "urls.txt"
    # NUM_MAIN_ENTITIES = 3
    # with open(URL_PATH, "r") as url_file:
    #     url_list = url_file.readlines()
    # raw_infos = get_scraped_infos(url_list)
    # raw_texts = [info["text"] for info in raw_infos]
    # entity_sentiments = list()
    # all_entities = list()
    # for text in raw_texts:
    #     text_entity_getter_instance = text_entity_getter(text)
    #     entity_sentiments.append({entity: get_doc_sentiment(text_entity_getter_instance.get_sentence_target_tuples(entity), net, embedding) for entity in text_entity_getter_instance.get_n_important_entities(NUM_MAIN_ENTITIES)[0]})
    #     all_entities.append(text_entity_getter_instance.get_unique_relevant_entities_stripped())
    # populate_database(generate_article_infos(raw_infos, entity_sentiments, all_entities), DB)
    net = load_model("models\\cnn.pkl")
    embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
    data = prep_twitter_data("data/acl-14-short-data/train.raw", "data/acl-14-short-data/test.raw")
    # retrain("models\\cnn12.09.2019.pkl", data, embedding)
    # for param in net.conv.parameters():
    #     param.requires_grad = False
    dir_path = "generate_article_data/article_datas"

    data = list()
    for article_data_path in os.listdir(dir_path):
        article_data = pkl.load(open(os.path.join("generate_article_data/article_datas", article_data_path), "rb"))
        data.extend(article_data)
    data = [i for i in data if i[1] != 0 or random.randint(1, 3) == 1]
    data = [list(i) for i in zip(*data)]
    print(sum(np.equal(get_sentiments(data[0], net, embedding), data[1]))/len(data[1]))
