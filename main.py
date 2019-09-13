from news_sentiment.doc_sentiment_analysis import *
from news_sentiment.cnn import *
# from populate_database import *
from preprocessing.article_entities import *
from news_sentiment.data_prep import *
import numpy as np
import random
import collections


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
    # net = load_model("models\\cnn.pkl")
    # data = prep_mpqa_data("data\\mpqa.raw")
    # retrain("models\\cnn13", data, embedding, epochs=3)
    dir_path = "generate_article_data/article_datas"

    data = list()
    for article_data_path in os.listdir(dir_path):
        article_data = pkl.load(open(os.path.join("generate_article_data/article_datas", article_data_path), "rb"))
        data.extend(article_data)
    data = [i for i in data if i[1] != 0 or random.randint(1, 5) <= 2]
    data = [list(i) for i in zip(*data)]
    input_data = prep_generated_data(data)

    embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
    retrain("models\\cnnyeet.pkl", input_data, embedding, num_epochs=30, batch_size=4)
    # print(sum(np.equal(get_sentiments(data[0], net, embedding), data[1]))/len(data[1]))
