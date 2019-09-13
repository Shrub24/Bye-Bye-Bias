from news_sentiment.cnn import *
from news_sentiment.data_prep import *
import numpy as np
import os


def get_sentiments(x, model, embed):
    x = input_prep(x)
    return [forward_prop([i], model, embed) for i in x]


def get_doc_sentiment(x, model, embed):
    scale = 9.0
    average_sentiment = np.average([i for i in get_sentiments(x, model, embed) if i != 0])
    return (average_sentiment + 1) * (scale/2) + 1


def load_model(PATH):
    model = Net()
    model.load_state_dict(torch.load(PATH))
    return model


def retrain(model_path, data, embed, freeze_conv=False, **kwargs):
    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        model = Net()
    if freeze_conv:
        model.freeze_conv_weights()
    train(model, *data, embed_model=embed, save_path=model_path, write=False, **kwargs)
    if freeze_conv:
        model.unfreeze_conv_weights()
    return model


# if __name__ == "__main__":
#     net = load_model("models\\cnn3.pkl")
#     embedding = load_embedding("embedding_model\\glove.twitter.27B.100d")
#     data = prep_mpqa_data("data\\mpqa.raw")
#     retrain("models\\cnn4.pkl", data, embedding)

    # define inputs
    # inputs = [["sentence", (i, j)], ...]
    # get_doc_sentiment(inputs, net, embedding)



