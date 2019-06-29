import random

import torch

from io import open
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_glove_model(file):
    print("Loading Glove Model")
    f = open(file, 'rb')
    model = {}
    for line in f.readlines():
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.", len(model), " words loaded!")
    return model


def prep_twitter_data(train, test):
    for data in [train, test]:
        with open(data, 'rb') as df:
            i = 0
            samples = list()
            sample = list()
            y = list()
            for line in df.readlines():
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
            if data == train:
                train_x = samples
                train_y = y
            else:
                test_x = samples
                test_y = y
    return train_x, train_y, test_x, test_y


def embed_to_tensor(b, embed_model, sentence_length, window_size, count, total):
    batch = np.array(b)
    x = list()
    x.append(list())
    x.append(list())
    for sample in batch:
        t_loc = 0
        sentence = list()
        length = sentence_length - (len(sample[1]) - 1) * sample[0].count(b'$T$')
        for i in range(length):
            if i < len(sample[0]):
                if sample[0][i] == b'$T$':
                    t_loc = i
                    if type(sample[1]) != np.ndarray and type(sample[1]) != list:
                        sample[1] = [sample[1]]
                    sentence += [get_embedding(i, embed_model, count, total) for i in sample[1]]
                else:
                    sentence.append(get_embedding(sample[0][i], embed_model, count, total))
            else:
                sentence.append(np.zeros(100))

        x[0].append(sentence)
        window = [np.zeros(100) for i in range(sentence_length)]
        window[t_loc-window_size:t_loc+len(sample[1])+window_size] = sentence[t_loc-window_size:t_loc+len(sample[1])+window_size]
        x[1].append(window)
    x = torch.tensor(x, dtype=torch.float32).transpose(0, 1)
    return x


def get_embedding(word, embed_model, count, total):
    total[0] += 1
    if type(word) != bytes:
        word = word.encode()
    try:
        return embed_model[word]
    except KeyError:
        count[0] += 1
        return np.zeros(100)
