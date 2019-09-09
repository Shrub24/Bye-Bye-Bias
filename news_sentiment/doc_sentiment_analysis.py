from cnn import *
from data_prep import *
import numpy as np


def get_sentiments(x, model):
    x = input_prep(x)
    return [forward_prop(i, model) for i in x]


def get_doc_sentiment(x, model):
    scale = 9.0
    average_sentiment = np.average(get_sentiments(x, model))
    return (average_sentiment + 1) * (scale/2) + 1


def load_model(PATH):
    net = Net()
    net.load_state_dict(torch.load(PATH))
    return net


if __name__ == "__main__":
    net = load_model("models\\cnn3.pkl")
    # define inputs
    # inputs = [["sentence", (i, j)], ...]
    # get_doc_sentiment(inputs, net)



