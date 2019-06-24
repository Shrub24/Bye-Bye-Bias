import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import GRU, Linear, Dropout
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


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.gru = GRU(100, 128, num_layers=1, bidirectional=True)
        self.fc1 = Linear(356, 128)
        self.fc2 = Linear(128, 3)
        self.dropout = Dropout(p=0.5)

    def forward(self, x, t):
        x = self.dropout(x)
        x = self.gru(x)
        x = x[0].view(max_sentence_length, -1, 2, 128)
        x_forward = x[max_sentence_length-1, :, 0, :][None, :, :]
        x_backward = x[max_sentence_length-1, :, 1, :][None, :, :]
        x = torch.cat((x_forward, t, x_backward), dim=2)
        x = self.dropout(x)
        x = F.relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=2)
        return x[0]


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


net = Net()
num_epochs = 4
lr = 0.001
batch_size = 4
label_names = ["negative, neutral, positive"]

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=lr)

data_path = "data\\acl-14-short-data"
train_path = os.path.join(data_path, "train.raw")
test_path = os.path.join(data_path, "test.raw")

train_x, train_y, test_x, test_y = prep_twitter_data(train_path, test_path,)

x_batches = [train_x[i:i+batch_size] for i in range(0, batch_size * int(len(train_x)/batch_size), batch_size)]
y_batches = [train_y[i:i+batch_size] for i in range(0, batch_size * int(len(train_y)/batch_size), batch_size)]


for epoch in range(num_epochs):
    running_loss = 0.0

    for i in range(len(x_batches)):
        x, t = embed_to_tensor(x_batches[i], model)

        labels = torch.tensor([j+1 for j in y_batches[i]], dtype=torch.long)

        optimizer.zero_grad()

        outputs = net(x, t)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        if i % 100 == 99:
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 100))
            running_loss = 0.0

    running_loss = 0.0
    correct = 0
    samples = 0

    with torch.no_grad():
        test_x_batches = [test_x[i:i + batch_size] for i in
                     range(0, batch_size * int(len(test_x) / batch_size), batch_size)]
        test_y_batches = [test_y[i:i + batch_size] for i in
                     range(0, batch_size * int(len(test_y) / batch_size), batch_size)]

        for i in range(len(test_x_batches)):
            x, t = embed_to_tensor(test_x_batches[i], model)

            labels = torch.tensor([j + 1 for j in test_y_batches[i]], dtype=torch.long)

            outputs = net(x, t)

            samples += batch_size
            correct += sum(torch.argmax(outputs) & labels)
            loss = criterion(outputs, labels)

            running_loss += loss.item()

    print('val_loss: %.3f, val_acc: %.2f' %
          (running_loss / int(len(test_x)/batch_size), float(correct)/samples), )
    running_loss = 0.0

    print("finished training!")

