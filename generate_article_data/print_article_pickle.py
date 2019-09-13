import pickle
import os

PICKLE_PATH = "article_data.pkl"
if os.path.isfile(PICKLE_PATH):
    print(pickle.load(open(PICKLE_PATH, "rb")))
else:
    print("file does not exist")