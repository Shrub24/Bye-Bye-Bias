from news_sentiment.cnn import *
from news_sentiment.data_prep import *
import numpy as np


def get_sentiments(x, model, embed):
    x = input_prep(x)
    return [forward_prop(i, model, embed) for i in x]


def get_doc_sentiment(x, model, embed):
    scale = 9.0
    average_sentiment = np.average(get_sentiments(x, model, embed))
    return (average_sentiment + 1) * (scale/2) + 1


def load_model(PATH):
    model = Net()
    model.load_state_dict(torch.load(PATH))
    return model


def retrain(model, data, embed):
    train(model, *data, embed_model=embed)


if __name__ == "__main__":
    net = load_model("models\\cnn3.pkl")
    embedding = load_embedding("embedding_model\\glove.twitter.27B.100d.txt")
    # define inputs
    # inputs = [["sentence", (i, j)], ...]
    # get_doc_sentiment(inputs, net, embedding)



