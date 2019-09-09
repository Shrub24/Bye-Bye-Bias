from cnn import *
from data_prep import *
import numpy as np


def get_sentiments(x):
    x = input_prep(x)
    return [forward_prop(i) for i in x]


def get_doc_sentiment(x):
    scale = 9.0
    average_sentiment = np.average(get_sentiments(x))
    return (average_sentiment + 1) * (scale/2) + 1


