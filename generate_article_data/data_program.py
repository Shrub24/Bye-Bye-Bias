import pickle as pkl

if __name__ == "__main__":
    SOURCE_PATH = "sentences.pkl"
    source = open(SOURCE_PATH, "rb")
    sentences = pkl.load(SOURCE_PATH)
    labelled_sentences = list()
    sentence_generator = (sentence, index for sentence, index in sentences)
    for sentence, index in sentence_generator:
        target = sentence[index[0]:index[1]]
        print(sentence[:index[0]] + "$T$" + sentence[index[1]:])
        print("target: " + target)
        label = input()
        if label in {"0", "1", "2"}:
            labelled_sentences.append(((sentence, index), int(label) - 1))
        elif label == "n":
            pass
        else:
            sentences = [(i, j) for i, j in sentence_generator]
    source = open(SOURCE_PATH, "wb")
    pkl.dump(sentences, SOURCE_PATH)

    PICKLE_PATH = "article_data.pkl"
    if os.path.isfile(PICKLE_PATH):
        pickled_data = pickle.load(open(PICKLE_PATH, "rb"))
        pickle.dump(pickled_data + labelled_sentences, open(PICKLE_PATH, "wb"))
    else:
        pickle.dump(labelled_sentences, open(PICKLE_PATH, "wb"))
