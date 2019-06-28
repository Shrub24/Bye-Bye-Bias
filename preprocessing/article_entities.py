# from newspaper import Article
import spacy

class entity_getter():
    def __init__(self):
        self.nlp = spacy.load("en")
        self.RELEVANT_ENTITY_TYPES = {"PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE"}
        self.DISALLOWED_CHARACTERS = {".", "'", "’", "@", "/"}

    def get_entities(self, text):
        document = self.nlp(text)
        return [ent for ent in document.ents]

    def get_unique_relevant_entities(self, text):
        document = self.nlp(text)
        return list({str(ent) for ent in document.ents if (ent.label_ in self.RELEVANT_ENTITY_TYPES)})

    def get_unique_relevant_entities_stripped(self, text):
        unique_relevant_entities = self.get_unique_relevant_entities(text)
        # remove entries that have disallowed characters
        unique_relevant_entities = [ent for ent in unique_relevant_entities if not any(x in ent for x in self.DISALLOWED_CHARACTERS)]
        # remove "the "
        return list({ent.replace("the ", "") for ent in unique_relevant_entities})

# def get_similarity_value(entities_a, entities_b):
#     similar = len(set(entities_a).intersection(entities_b))
#     unique = len(entities_a) + len(entities_b) - (2 * similar)
#     return similar/(similar + unique)
#
# entity_getter_instance = entity_getter()
# entity_list = list()
# urls = ["https://www.usatoday.com/story/news/politics/2019/06/20/oregon-senate-republicans-gop-walk-out-capitol-second-time-house-bill-2020/1517308001/", "https://www.vox.com/2019/6/21/18700741/oregon-republican-walkout-climate-change-bill", "https://www.apnews.com/9783213088c845beaa379f4a17128790", "https://www.cbsnews.com/news/oregon-senate-walkout-more-than-100-bills-in-jeopardy-as-gop-senators-stay-in-hiding/"]
# for url in urls:
#     article = Article(url)
#     article.download()
#     article.parse()
#     print(entity_getter_instance.get_unique_relevant_entities_stripped(article.text))
#     entity_list.append(entity_getter_instance.get_unique_relevant_entities_stripped(article.text))
#
# for i in entity_list:
#     for j in entity_list:
#         print(get_similarity_value(i, j))
