from news_sentiment.doc_sentiment_analysis import *
from news_sentiment.cnn import *
from populate_database import *
from preprocessing.article_entities import entity_getter

if __name__ == "__main__":
    # net = load_model("models\\cnn7.pkl")
    embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
    # data = prep_mpqa_data("data\\mpqa.raw")
    data = prep_twitter_data("data\\acl-14-short-data\\train.raw", "data\\acl-14-short-data\\test.raw")
    retrain("models\\cnn8.pkl", data, embedding)
    # while True:
    #     sentence = input("input a sentence: ")
    #     target = input("input a target: ")
    #     t_loc = sentence.find(target)
    #     indexes = (t_loc, t_loc+len(target))
    #     print(get_sentiments([(sentence, indexes)], net, embedding))

    # generate_mpqa_data("data\\database.mpqa.2.0", "data\\mpqa.raw")

    # URL_PATH = "urls.txt"
    # NUM_MAIN_ENTITIES = 3
    # entity_getter_instance = entity_getter()
    # with open(URL_PATH, "r") as url_file:
    #     url_list = url_file.readlines()
    # raw_infos = get_scraped_infos(url_list)
    # raw_texts = [info["text"] for info in raw_infos]
    # entity_sentiments = [{entity: get_doc_sentiment(entity_getter_instance.get_sentence_target_tuples(text, entity), net, embedding) for entity in entity_getter_instance.get_n_important_entities(text, NUM_MAIN_ENTITIES)} for text in raw_texts]
    # populate_database(generate_article_infos(raw_infos, entity_sentiments, get_all_entities(raw_texts, entity_getter_instance)))
