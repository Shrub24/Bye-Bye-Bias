import torch

import os
from io import open
import numpy as np
import pickle as pkl

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