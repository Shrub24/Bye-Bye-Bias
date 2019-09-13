import pickle as pkl
import os
import itertools

if __name__ == "__main__":
    SOURCE_PATH = "sentences3.pkl"
    source = open(SOURCE_PATH, "rb")
    sentences = pkl.load(source)
    sentences = sentences
    labelled_sentences = list()
    # sentences = list(set(sentences))
    # sentences = list(itertools.chain.from_iterable(sentences))
    sentence_generator = ((sentence[0], sentence[1]) for sentence in sentences)
    temp = list()
    for sentence, index in sentence_generator:
        target = sentence[index[0]:index[1]]
        print(sentence[:index[0]] + "$T$" + sentence[index[1]:])
        print("target: " + target)
        label = input()
        if label in {"-1", "0", "1"}:
            labelled_sentences.append(((sentence, index), int(label)))
        elif label == "n":
            pass
        else:
            temp = [(sentence, index)]
            temp.extend([(i, j) for i, j in sentence_generator])
            break
    source = open(SOURCE_PATH, "wb")
    pkl.dump(temp, source)

    PICKLE_PATH = "article_data.pkl"
    if os.path.isfile(PICKLE_PATH):
        pickled_data = pkl.load(open(PICKLE_PATH, "rb"))
        pkl.dump(pickled_data + labelled_sentences, open(PICKLE_PATH, "wb"))
    else:
        pkl.dump(labelled_sentences, open(PICKLE_PATH, "wb"))

    # SOURCE_PATH = "sentences4.pkl"
    # source = open(SOURCE_PATH, "rb")
    # sentences = pkl.load(source)
    # sentences = set(sentences)
    # temp = list()
    # for sentence, index in sentences:
    #     target = sentence[index[0]:index[1]]
    #     if "it" not in target:
    #         if target.strip() != "'s":
    #             if target[-2:] == "'s":
    #                 temp.append((sentence, (index[0], index[1]-2)))
    #             else:
    #                 temp.append((sentence, index))
    # source = open(SOURCE_PATH, "wb")
    # pkl.dump(temp, source)
