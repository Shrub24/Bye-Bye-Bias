from news_sentiment.doc_sentiment_analysis import *
from news_sentiment.cnn import *
from populate_database import *
from preprocessing.article_entities import entity_getter

if __name__ == "__main__":
    net = load_model("models\\cnn3.pkl")
    embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
    URL_PATH = "urls.txt"
    NUM_MAIN_ENTITIES = 3
    entity_getter_instance = entity_getter()
    with open(URL_PATH, "r") as url_file:
        url_list = url_file.readlines()
    raw_infos = get_scraped_infos(url_list)
    raw_texts = [info["text"] for info in raw_infos]
    entity_sentiments = [{entity: get_doc_sentiment(entity_getter_instance.get_sentence_target_tuples(text, entity), net, embedding) for entity in entity_getter_instance.get_n_important_entities(text, NUM_MAIN_ENTITIES)} for text in raw_texts]
    populate_database(generate_article_infos(raw_infos, entity_sentiments, get_all_entities(raw_texts, entity_getter_instance)))