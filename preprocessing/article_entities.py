from newspaper import Article
import spacy
import neuralcoref

class entity_getter():
    def __init__(self):
        self.nlp = spacy.load("en")
        neuralcoref.add_to_pipe(self.nlp, greedyness=0.54, max_dist=100)
        self.RELEVANT_ENTITY_TYPES = {"PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE"}
        self.ALLOWED_ENTITY_TYPES_MAIN_ENTITIES = {"PERSON", "NORP", "FAC", "ORG", "PRODUCT", "EVENT", "WORk_OF_ART", "LAW"}
        self.DISALLOWED_CHARACTERS = {".", "'", "’", "@", "/"}
        self.ACCEPTABLE_POS_IN_ENTITIES = {"NOUN", "PROPN"}
        # self.TITLES = {"mr", "mr.", "ms", "ms.", "miss", "master", "madam", "mp", "representative", "senator", "speaker", "president", "councillor", "mayor", "governor", "premier", "secretary", "king", "prince", "justice", "doctor", "dr", "dr.", "professor", "prof."}
        self.ENTITY_LENGTH_CAP = 3

    def get_entities(self, text):
        document = self.nlp(text)
        return [ent for ent in document.ents]

    def get_unique_relevant_entities(self, text, relevant_types):
        document = self.nlp(text)
        # print({str(ent): ent.label_ for ent in document.ents})
        return list({str(ent) for ent in document.ents if (ent.label_ in relevant_types)})

    def get_unique_relevant_entities_stripped(self, text):
        unique_relevant_entities = self.get_unique_relevant_entities(text, self.RELEVANT_ENTITY_TYPES)
        # remove entries that have disallowed characters
        unique_relevant_entities = [ent for ent in unique_relevant_entities if not any(x in ent for x in self.DISALLOWED_CHARACTERS)]
        # remove "the "
        return list({ent[4:] if ent.startswith("the ") else ent for ent in unique_relevant_entities})

    def get_allowed_entities_for_main_stripped(self, text):
        unique_relevant_entities = self.get_unique_relevant_entities(text, self.ALLOWED_ENTITY_TYPES_MAIN_ENTITIES)
        # remove entries that have disallowed characters
        unique_relevant_entities = [ent for ent in unique_relevant_entities if not any(x in ent for x in self.DISALLOWED_CHARACTERS)]
        # remove "the "
        return list({ent[4:] if ent.startswith("the ") else ent for ent in unique_relevant_entities})

    def get_pos_tags(self, text):
        document = self.nlp(text)
        return {token.text: token.pos_ for token in document}

    # todo refactor
    def get_n_important_entities(self, text, n):
        document = self.nlp(text)
        entity_occurences = dict()
        for cluster in document._.coref_clusters:
            raw_entity_string = str(cluster.main)
            occurences = len(cluster)
            # if discernible ners add ners to entities
            ners = self.get_allowed_entities_for_main_stripped(raw_entity_string)
            if ners:
                entities = ners
            # otherwise get pos tags and find nouns
            else:
                # pos_tags = self.get_pos_tags(raw_entity_string)
                # # construct just nouns string
                # entity_string = ""
                # for word in pos_tags.keys():
                #     if pos_tags[word] in self.ACCEPTABLE_POS_IN_ENTITIES:
                #         entity_string += word + " "
                # if entity_string:
                #     entities = [entity_string[:-1]]
                # else:
                #     entities = []
                entities = []
            for entity in entities:
                # check entity is long enough and lowercase everything in final dict
                if len(entity.split()) <= self.ENTITY_LENGTH_CAP:
                    if entity.lower() in entity_occurences:
                        entity_occurences[entity.lower()] += occurences
                    else:
                        entity_occurences[entity.lower()] = occurences
        return sorted(list(entity_occurences.keys()), key=lambda x: entity_occurences[x], reverse=True)[:n]
        # clusters_by_len = sorted(document._.coref_clusters, key=len, reverse=True)[:n]
        # return [cluster.main for cluster in clusters_by_len]

    # def get_coreferences(self, text, string):
    #     document = self.nlp(text)
    #     return [token._.coref_clusters[0].mentions for token in document if string == str(token).lower() and token._.in_coref]
    #     # return list({token._.coref_clusters.mentions[0] for token in document if string in str(token).lower() and token._.in_coref})
    #



# def get_similarity_value(entities_a, entities_b):
#     similar = len(set(entities_a).intersection(entities_b))
#     unique = len(entities_a) + len(entities_b) - (2 * similar)
#     return similar/(similar + unique)
#
# entity_getter_instance = entity_getter()
# urls = ["https://www.usatoday.com/story/news/politics/2019/06/20/oregon-senate-republicans-gop-walk-out-capitol-second-time-house-bill-2020/1517308001/", "https://www.vox.com/2019/6/21/18700741/oregon-republican-walkout-climate-change-bill", "https://www.apnews.com/9783213088c845beaa379f4a17128790", "https://www.cbsnews.com/news/oregon-senate-walkout-more-than-100-bills-in-jeopardy-as-gop-senators-stay-in-hiding/"]
# urls = ["https://www.cnbc.com/2019/06/28/trump-and-xi-to-discuss-us-china-trade-war-at-g-20-summit-in-osaka.html", "https://www.scmp.com/news/china/diplomacy/article/3016167/us-china-trade-war-deal-90-cent-complete-us-treasury-chief", "https://www.aljazeera.com/ajimpact/christmas-cancelled-chinese-factories-feel-chill-trade-190627144329359.html", "https://edition.cnn.com/2019/06/27/politics/china-us-trade-war-trump-xi-intl-hnk/index.html"]
# urls = ["https://www.abc.net.au/news/2019-06-28/don-burke-defeats-wendy-dent-defamation-action/11260302", "https://www.abc.net.au/news/2019-06-28/consumer-watchdog-loses-flushable-wipes-case/11261688", "https://www.abc.net.au/news/2019-06-28/rotorua-mud-pool-opens-whakarewarewa-backyard-new-zealand/11262272", "https://www.abc.net.au/news/2019-06-28/sirius-building-sold-to-developers-for-150-million-dollars/11262638", "https://www.abc.net.au/news/2019-06-28/trump-asks-putin-not-to-meddle-in-the-us-election/11262976", "https://www.abc.net.au/news/2019-06-28/five-takeaways-from-the-democratic-debates/11260074", "https://www.abc.net.au/news/2019-06-28/two-dead-in-wollongong-princes-motorway-crash/11262688", "https://www.abc.net.au/news/2019-06-28/the-g20-will-really-be-about-donald-trump-and-xi-jinping/11256802"]
# for url in urls:
#     article = Article(url)
#     article.download()
#     article.parse()
#     entities = entity_getter_instance.get_n_important_entities(article.text, 6)
#     print(entities)
#     print(entity_getter_instance.get_coreferences(article.text, entities[0]))

#
# for i in entity_list:
#     for j in entity_list:
#         print(get_similarity_value(i, j))

