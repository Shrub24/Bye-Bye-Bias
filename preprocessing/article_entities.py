from newspaper import Article
import spacy
import neuralcoref
import re
import copy
from collections import defaultdict
import itertools

class entity_getter():
    def __init__(self):
        self.nlp = spacy.load("en")
        neuralcoref.add_to_pipe(self.nlp, greedyness=0.54, max_dist=100)
        self.RELEVANT_ENTITY_TYPES = {"PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "WORK_OF_ART", "LAW", "LANGUAGE"}
        self.ALLOWED_ENTITY_TYPES_MAIN_ENTITIES = {"PERSON", "NORP", "FAC", "ORG", "PRODUCT", "EVENT", "WORk_OF_ART", "LAW"}
        self.DISALLOWED_CHARACTERS = {".", "'", "'", "@", "/"}
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
        # get entities and format person
        relevant_types = self.ALLOWED_ENTITY_TYPES_MAIN_ENTITIES
        document = self.nlp(text)
        entities = set()
        for ent in document.ents:
            # print(str(ent).split())
            if ent.label_ == "PERSON":
                entities = entities.union({str(ent).split()[-1]})
            elif ent.label_ in relevant_types:
                # print(entities.union(str(ent)))
                entities = entities.union({str(ent)})
        # print(entities)
        # format and filter entities
        unique_relevant_entities = entities
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


class text_entity_getter(entity_getter):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.document = self.nlp(text)


    def get_unique_relevant_entities_stripped(self):
        unique_relevant_entities = list({str(ent) for ent in self.document.ents if (ent.label_ in self.RELEVANT_ENTITY_TYPES)})
        # remove entries that have disallowed characters
        unique_relevant_entities = [ent for ent in unique_relevant_entities if not any(x in ent for x in self.DISALLOWED_CHARACTERS)]
        # remove "the "
        return list({ent[4:] if ent.startswith("the ") else ent for ent in unique_relevant_entities})

    def a_in_b_span(self, a, b):
        if a.start <= b.start and b.end >= a.end:
            return True
        return False

    def find_sentence(self, sentences, span):
        for sentence in sentences:
            if a_in_b_span(span, sentence):
                return sentence
        return None

    def get_n_important_entities(self, n):
        entity_tokens = defaultdict(list)
        entity_occurences = dict()
        entity_sentences = {}
        for cluster in self.document._.coref_clusters:
            raw_entity_string = str(cluster.main)
            # if discernible ners add ners to entities
            ners = cluster.main.ents
            if ners:
                entities = ners
            else:
                entities = []
            for ner in entities:
                if ner.label_ in self.RELEVANT_ENTITY_TYPES and not any(x in str(ner) for x in self.DISALLOWED_CHARACTERS):
                    entity = self.format_main_ent_to_string(ner)
                    # check entity is short enough and lowercase everything in final dict
                    if len(entity.split()) <= self.ENTITY_LENGTH_CAP:
                        if entity in entity_occurences:
                            entity_sentences[entity] = entity_sentences[entity].union(set([i.sent for i in cluster]))
                        else:
                            entity_sentences[entity] = set([i.sent for i in cluster])
                        entity_tokens[entity].append(ner)
        for key in entity_sentences.keys():
            entity_occurences[(key, tuple(entity_tokens[key]))] = len(entity_sentences[key])
        return sorted(list(entity_occurences.keys()), key=lambda x: entity_occurences[x], reverse=True)[:n]


    def get_sentence_target_tuples_from_tokens(self, ents):
        mentions = set()
        sentence_targets = defaultdict(list)

        for ent in ents:
            if ent._.is_coref:
                mentions = mentions.union(set(ent._.coref_cluster.mentions))
            sentence = ent.sent
            sentence_targets[sentence].append(ent)

        for mention in mentions:
            sentence = mention.sent
            if sentence not in sentence_targets:
                if not any((stuff == mention.text.strip() for stuff in ["it", "", "its", "it's", "'s"])):
                    sentence_targets[sentence] = [mention]

        sentence_target_tuples = list()

        for sentence, targets in sentence_targets.items():
            out_sentence = sentence.text.strip()
            targets = set(targets)
            for target in targets:
                out_target = target
                if target.text[-2:] == "'s":
                    out_target = target[:-2]
                sentence_target_tuples.append((out_sentence.strip("\n").strip(), (out_target.start_char - sentence.start_char, out_target.end_char - sentence.start_char)))

        #
        # for sentence, index in sentence_target_tuples:
        #     target = sentence[index[0]:index[1]]
        #     print(sentence[:index[0]] + "-" * (index[1] - index[0]) + sentence[index[1]:])
        #     print(target)

        return sentence_target_tuples



    def get_sentence_target_tuples(self, string):
        split_string = string.split()
        string_length = len(split_string)
        current_indexes = dict()
        sentence_target_tuples = list()

        for i, token in enumerate(self.document):
            # if single word input
            if string_length == 1 and string == str(token).lower() and token._.in_coref:
                mentions = token._.coref_clusters[0].mentions
            # if multiple word input
            # todo refactor elif?
            elif string_length > 1:
                span = self.document[i:i + string_length]
                cur_span_is_equal = (split_string == [str(token).lower() for token in span])
                if cur_span_is_equal and span._.is_coref:
                    mentions = span._.coref_cluster.mentions
                else:
                    # add span to target if no coreference
                    index_location = (span[0].idx, span[-1].idx + len(span[-1]))
                    if cur_span_is_equal and index_location not in current_indexes:
                        sentence = span.sent
                        current_indexes[index_location] = True
                        sentence_target_tuples.append((str(sentence), (index_location[0] - sentence.start_char, index_location[1] - sentence.start_char)))
                    mentions = []
            else:
                mentions = []
            for cluster_token_span in mentions:
                if len(cluster_token_span) <= self.ENTITY_LENGTH_CAP:
                    sentence = cluster_token_span.sent
                    last_length = len(cluster_token_span[-1])
                    index_location = (cluster_token_span[0].idx, cluster_token_span[-1].idx + last_length)
                    if index_location not in current_indexes:
                        current_indexes[index_location] = True
                        sentence_target_tuples.append((str(sentence), (index_location[0] - sentence.start_char, index_location[1] - sentence.start_char)))
        return sentence_target_tuples

    def format_main_ent_to_string(self, ent):
        string = str(ent).lower()
        if string.startswith("the "):
            string = string[4:]
        if ent.label_ == "PERSON":
            string = string.split()[-1]
        return string



# def format_text(target_locations, text):
#     REPLACE_STRING = "$T$"
#     ret_text = text
#     target_list = list()
#     length_diff = 0
#     for location in target_locations:
#         target = text[location[0]:location[1]]
#         target_list.append(target)
#         ret_text = ret_text[0:location[0] + length_diff] + "$T$" + ret_text[location[1] + length_diff:]
#         length_diff += len(REPLACE_STRING) - len(target)
#     return ret_text, target_list



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
#     # print(entities)
#     print(entities[0])
#     # print(entity_getter_instance.get_coreferences(article.text, entities[0]))
#     # coreference_index = entity_getter_instance.get_coreferences(article.text, entities[0])
#     # txt = article.text
#     # for i in coreference_index:
#     #     txt = txt[0:i[0]] + "-" * (i[1] - i[0]) + txt[i[1]:]
#     # print(txt)
#     ret = entity_getter_instance.get_sentence_target_lists(article.text, entities[0])
#     for i, val in enumerate(ret[0]):
#         print(val[:ret[1][i][0]] + "$T$" + val[ret[1][i][1]:])

#
# for i in entity_list:
#     for j in entity_list:
#         print(get_similarity_value(i, j))

