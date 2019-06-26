import torch

import os
from io import open
import numpy as np
import pickle as pkl
import re

embedding_name = "glove.twitter.27B.100d"
embedding = os.path.join("embeddings", embedding_name + ".txt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

zero_count = 0


def load_glove_model(file):
    print("Loading Glove Model")
    f = open(file, 'rb')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.", len(model), " words loaded!")
    return model


try:
    file = open(os.path.join("embedding_model", embedding_name), 'rb')
    model = pkl.load(file)
except FileNotFoundError:
    model = load_glove_model(embedding)
    file = open(os.path.join("embedding_model", embedding_name), 'wb')
    pkl.dump(model, file)


max_sentence_length = 30
dp = 0.5


def prep_twitter_data(train, test):
    for data in [train, test]:
        with open(data, 'rb') as df:
            i = 0
            samples = list()
            sample = list()
            y = list()
            for line in df:
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
            if data == train:
                train_x = samples
                train_y = y
            else:
                test_x = samples
                test_y = y
    return train_x, train_y, test_x, test_y


def embed_to_tensor(b, embed_model):
    # batch = b.copy()
    batch = np.array(b)
    for sample in batch:
        if (type(sample[1]) is np.ndarray) or (type(sample[1]) is list):
            embeddings = [get_embedding(s, embed_model) for s in sample[1]]
            sample[1] = sum(embeddings)/len(embeddings)
        else:
            sample[1] = get_embedding(sample[1], embed_model)
        for i in range(30):
            if i < len(sample[0]):
                temp = list()
                temp.append(sample[1][i] if sample[0][i] == "$T$" else get_embedding(sample[0][i], embed_model))
            else:
                temp.append(np.zeros(100))
            sample[0] = temp
    x = [sample[0] for sample in batch]
    t = [sample[1] for sample in batch]
    x = torch.tensor(x, dtype=torch.float32).transpose(0, 1)
    t = torch.tensor(t, dtype=torch.float32)[None, :, :]
    return x, t


def get_embedding(word, embed_model):
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
                    # if (not j.find("GATE_attitude") == -1) and (j.find("speculation") == -1) and (j.find("other-attitude") == -1):
                    if (not j.find("GATE_attitude") == -1) and (not j.find("sentiment-pos") == -1 or not j.find("sentiment-neg") == -1):
                        attitude_properties = dict()
                        attitude_properties["byte"] = j.split("\t")[1].split(",")
                        properties = j.split("\t")[-1].strip().split('" ')
                        for k in properties:
                            split_prop = k.split('="')
                            if split_prop[1].find(",") == -1:
                                attitude_properties[split_prop[0]] = split_prop[1]
                            else:
                                attitude_properties[split_prop[0]] = [l.strip() for l in split_prop[1].split(",")]
                        attitude_anns.append(attitude_properties)

                    elif not j.find("GATE_target") == -1:
                        space_split = j.split()
                        target_bytes[space_split[4][4:-1]] = space_split[1].split(",")

            # print(target_bytes)
            # print(attitude_anns)
            SENTENCES_PATH = script_dir + MAN_ANNS_REL_PATH + file + "/" + SENTENCES_FILE_NAME
            with open(script_dir + DOCS_REL_PATH + file) as doc_file:
                file_string = doc_file.read().replace("\n", " ").replace("\t", " ")
                for attitude in attitude_anns:
                    targets = attitude["target-link"]
                    if not targets == "none":
                        if not isinstance(targets, list):
                            targets = [targets]
                        for target in targets:
                            target_loc = [int(j) for j in target_bytes[target]]
                            sentence_bytes = find_sentence_bytes(target_loc[0], SENTENCES_PATH)
                            sentence = file_string[sentence_bytes[0]:sentence_bytes[1]].replace("  ", " ")
                            target = file_string[target_loc[0]:target_loc[1]].replace("  ", " ")
                            new_target = re.sub('(?<! )(?=[][.,!?():;\"\'-])|(?<=[][.,!?():;\"\'-])(?! )', r' ', target).strip()
                            sentiment = get_sentiment_pos_neg(attitude["attitude-type"])
                            # space punctuation marks then check that target is isolated word
                            new_sentence = " " + re.sub('(?<! )(?=[][.,!?():;\"\'-])|(?<=[][.,!?():;\"\'-])(?! )', r' ', sentence) + " "
                            new_sentence = new_sentence.replace(" " + new_target + " ", " $T$ ").strip()
                            print("sentence: " + new_sentence)
                            print("target: " + target)
                            print("sentiment: " + str(sentiment))
                            print("")
                            if len(target.split()) <= 5 and new_sentence.count("$T$") == 1:
                                with open(OUT_PATH, "a") as write_file:
                                    write_file.write(new_sentence + "\n")
                                    write_file.write(target + "\n")
                                    write_file.write(str(sentiment) + "\n")



def find_sentence_bytes(byte_within, path):
    with open(path) as sentences_file:
        lowest = None
        lowest_compare = None
        for i in sentences_file:
            bytes = [int(j) for j in i.split("\t")[1].split(",")]
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



generate_mpqa_data("/data/database.mpqa.2.0/", "/data/mpqa.raw")
