from news_sentiment.tdbert import *
from news_sentiment.data_prep import *
import numpy as np
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_sentiments(x, model):
    x = bert_input_prep(x)
    return [forward_prop([i], model) for i in x]


def get_sentiments_backup(x):
    if "trump" in x:
        return -1
    else:
        random.randint(0, 1)


def get_doc_sentiment(x, model):
    scale = 9.0
    average_sentiment = np.average([i for i in get_sentiments(x, model, embed)])
    return (average_sentiment + 1) * (scale/2) + 1


def load_model(PATH):
    model = Net()
    model.load_state_dict(torch.load(PATH))
    return model


def retrain(model_path, data, **kwargs):
    if os.path.exists(model_path):
        model = load_model(model_path)
        model.to(device)
    else:
        model = Net()
        model = model.to(device)
    train(model, *data, save_path=model_path, **kwargs)
    return model


if __name__ == "__main__":
    data = prep_mpqa_data(".\\data\\mpqa.raw")
    retrain("models\\bert2.pkl", data, num_epochs=20, write=True)



