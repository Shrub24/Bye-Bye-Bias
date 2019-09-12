import itertools
import random

import torch

from io import open
import numpy as np
import pickle as pkl
import re
import os
import spacy
nlp = spacy.load("en")

embedding_name = "glove.twitter.27B.100d"
embedding = os.path.join("embeddings", embedding_name + ".txt")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_glove_model(file):
    print("Loading Glove Model")
    f = open(file, 'rb')
    model = {}
    for line in f.readlines():
        splitLine = line.split()
        word = splitLine[0].decode()
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.", len(model), " words loaded!")
    return model


def prep_data(train, test):
    for dataset in [train, test]:
            i = 0
            samples = list()
            sample = list()
            y = list()
            for line in dataset:
                if i % 3 == 0:
                    if i != 0:
                        samples.append(sample)
                        sample = list()
                    sample.append(line.split())
                elif i % 3 == 2:
                    y.append(int(line))
                elif i % 3 == 1:
                    sample.append(line.split())
                else:
                    sample.append(line)
                i += 1
            temp = list(zip(samples, y))

            random.shuffle(temp)

            samples, y = zip(*temp)
            if dataset == train:
                train_x = samples
                train_y = y
            else:
                test_x = samples
                test_y = y
    return train_x, train_y, test_x, test_y


def prep_twitter_data(train, test):
        train = open(train, 'rb').readlines()
        test = open(test, 'rb').readlines()
        return prep_data(train, test)


def prep_mpqa_data(dataset):
    temp = open(dataset, 'rb').readlines()
    data = [temp[i:i + 3] for i in range(0, len(temp), 3)]
    random.shuffle(data)
    data = list(itertools.chain.from_iterable(data))
    test = data[-3 * 400:]
    train = data[:-3 * 400]
    return prep_data(train, test)


def embed_to_tensor(b, embed_model, sentence_length, window_size):
    batch = np.array(b)
    x = list()
    x.append(list())
    x.append(list())
    for sample in batch:
        t_loc = 0
        sentence = list()
        sentence = sentence[:sentence_length]

        length = sentence_length - (len(sample[1]) - 1) # * list(sample[0]).count(b'$T$')
        for i in range(length):
            if i < len(sample[0]):
                if sample[0][i] == b'$T$' or sample[0][i] == "$T$":
                    t_loc = i
                    if type(sample[1]) != np.ndarray and type(sample[1]) != list:
                        sample[1] = [sample[1]]
                    sentence.extend([get_embedding(j, embed_model) for j in sample[1]])
                else:
                    sentence.append(get_embedding(sample[0][i], embed_model))
            else:
                sentence.append(np.zeros(100))

        x[0].append(sentence)
        window = [np.zeros(100) for i in range(sentence_length)]
        window[t_loc-window_size:t_loc+len(sample[1])+window_size] = sentence[t_loc-window_size:t_loc+len(sample[1])+window_size]
        x[1].append(window)
    x = torch.tensor(x, dtype=torch.float32).transpose(0, 1)
    return x


def get_embedding(word, embed_model):
    if type(word) != bytes and type(word) != np.bytes_:
        word = word.encode()
    try:
        return embed_model[word]
    except KeyError:
      return np.zeros(100)


# path = "/data/database.mpqa.2.0/"
def generate_mpqa_data(path, out_path):
    script_dir = os.path.dirname(__file__)
    OUT_PATH = script_dir + out_path
    if os.path.exists(OUT_PATH):
        os.remove(OUT_PATH)
    file = open(OUT_PATH, "x")
    file.close()
    MPQA_REL_PATH = path
    DOCS_REL_PATH = MPQA_REL_PATH + "docs/"
    MAN_ANNS_REL_PATH = MPQA_REL_PATH + "man_anns/"
    ANNOTATION_FILE_NAME = "gateman.mpqa.lre.2.0"
    SENTENCES_FILE_NAME = "gatesentences.mpqa.2.0"

    with open(script_dir + MPQA_REL_PATH + "doclist.mpqaOriginalByTopic", "r") as topic_file:
        for i in topic_file:
            split = i.split()
            topic = split[0][6:]
            file = split[1][5:]
            with open(script_dir + MAN_ANNS_REL_PATH + file + "/" + ANNOTATION_FILE_NAME) as anns_file:
                attitude_anns = list()
                target_bytes = dict()
                for j in anns_file:
                    if any(s in j for s in ["pos", "neg", "other-attitude"]) and "GATE_attitude" in j:
                        attitude_properties = dict()
                        elements = j.split("\t")
                        attitude_properties["byte"] = elements[1].split(",")
                        properties = elements[-1].strip().split('" ')
                        for k in properties:
                            split_prop = k.split('="')
                            if "," not in split_prop[1]:
                                attitude_properties[split_prop[0]] = split_prop[1]
                            else:
                                attitude_properties[split_prop[0]] = [l.strip() for l in split_prop[1].split(",")]
                        attitude_anns.append(attitude_properties)

                    elif "GATE_target" in j:
                        space_split = j.split()
                        target_bytes[space_split[4][4:-1]] = space_split[1].split(",")

            SENTENCES_PATH = script_dir + MAN_ANNS_REL_PATH + file + "/" + SENTENCES_FILE_NAME
            with open(script_dir + DOCS_REL_PATH + file) as doc_file:
                file_string = doc_file.read().replace("\n", " ").replace("\t", " ")
                generate_mpqa_neutrals(file_string, attitude_anns, target_bytes, SENTENCES_PATH, OUT_PATH)
                attitude_anns = [attitude for attitude in attitude_anns if "sentiment" in attitude["attitude-type"]]
                for attitude in attitude_anns:
                    targets = attitude["target-link"]
                    if not targets == "none":
                        if not isinstance(targets, list):
                            targets = [targets]
                        targets = [target for target in targets if target in target_bytes]
                        for target in targets:
                            target_loc = [int(j) for j in target_bytes[target]]
                            sentence_bytes = find_sentence_bytes(target_loc[0], SENTENCES_PATH)
                            sentence = file_string[sentence_bytes[0]:sentence_bytes[1]].replace("  ", " ")
                            target = file_string[target_loc[0]:target_loc[1]].replace("  ", " ")
                            new_target = re.sub('(?<! )(?=[][.,!?():;\"\'-])|(?<=[][.,!?():;\"\'-])(?! )', r' ', target).strip()
                            sentiment = get_sentiment_pos_neg(attitude["attitude-type"])
                            # space punctuation marks then check that target is isolated word
                            new_sentence = " " + re.sub('(?<! )(?=[][.,!?():;\"\'-])|(?<=[][.,!?():;\"\'-])(?! )', r' ', sentence) + " "
                            new_sentence = new_sentence.replace(" " + new_target + " ", " " + "$T$" + " ").strip()
                            if len(target.split()) <= 5 and new_sentence.count("$T$") == 1:
                                with open(OUT_PATH, "a") as write_file:
                                    write_file.write(new_sentence + "\n")
                                    write_file.write(target + "\n")
                                    write_file.write(str(sentiment) + "\n")


def tokenise(sentence):
    return re.sub('(?<! )(?=[][.,!?():;\"\'-])|(?<=[][.,!?():;\"\'-])(?! )', r' ', sentence)


def train_sentence_prep(sentence, target):
    temp = " " + tokenise(sentence) + " "
    temp = temp.replace(" " + target + " ", " " + "$T$" + " ").strip().strip(".").strip()
    return temp


def sentence_prep(sentence, target_indexes):
    temp = sentence[:target_indexes[0]] + "$T$" + sentence[target_indexes[1]:]
    target = sentence[target_indexes[0]:target_indexes[1]]
    temp = tokenise(temp)
    target = tokenise(target)
    return temp, target


def input_prep(x):
    prepped = list()
    for sample in x:
        prepped_sample = list(map(lambda x: x.split(), sentence_prep(sample[0], sample[1])))
        prepped.append(prepped_sample)
    return prepped


def generate_mpqa_neutrals(file_string, attitude_anns, target_bytes, sentence_path, out_path):
    sentence_bytes = set()
    sentences = list()
    for i in open(sentence_path):
        bytes = tuple(map(int, i.split("\t")[1].split(",")))
        sentence_bytes.add(bytes)
    for attitude in attitude_anns:
        targets = attitude["target-link"]
        if not targets == "none":
            if not isinstance(targets, list):
                targets = [targets]
            targets = [target for target in targets if target in target_bytes]
            for target in targets:
                target_loc = [int(j) for j in target_bytes[target]]
                target_sentence_bytes = find_sentence_bytes(target_loc[0], sentence_path)
                if target_sentence_bytes in sentence_bytes:
                    sentence_bytes.remove(target_sentence_bytes)
    for bytes in sentence_bytes:
        sentence = file_string[bytes[0]:bytes[1]].replace("  ", " ")
        target = get_entity(sentence)
        if target is None:
            break
        new_sentence = train_sentence_prep(sentence, target)
        if len(target.split()) <= 5 and new_sentence.count("$T$") == 1:
            with open(out_path, "a") as write_file:
                write_file.write(new_sentence + "\n")
                write_file.write(target + "\n")
                write_file.write(str(0) + "\n")


def get_entity(sentence):
    doc = nlp(sentence)
    subjects = [str(tok) for tok in doc if (tok.dep_ == "nsubj")]
    return random.choice(subjects) if subjects else None


def find_sentence_bytes(byte_within, path):
    with open(path) as sentences_file:
        lowest = None
        lowest_compare = None
        for i in sentences_file:
            bytes = tuple(map(int, i.split("\t")[1].split(",")))
            compare = byte_within - bytes[0]
            if compare >= 0:
                if (lowest is None) or (compare < lowest_compare):
                    lowest = bytes
                    lowest_compare = compare
    return lowest


def get_sentiment_pos_neg(sentiment_string):
    if sentiment_string == "sentiment-pos":
        return 1
    elif sentiment_string == "sentiment-neg":
        return -1
    else:
        return 0


# generate_mpqa_data("/data/database.mpqa.2.0/", "/data/mpqa.raw")
