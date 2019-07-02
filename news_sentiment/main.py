import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import GRU, Linear, Dropout
import os
from io import open
import numpy as np
from data_prep import *

import pickle as pkl

count = list()
count.append(0)

total = list()
total.append(0)

EMBEDDING_NAME = "glove.twitter.27B.100d"
EMBEDDING = os.path.join("embeddings", EMBEDDING_NAME + ".txt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

try:
    file = open(os.path.join("embedding_model", EMBEDDING_NAME), 'rb')
    model = pkl.load(file)
except FileNotFoundError:
    model = load_glove_model(EMBEDDING)
    file = open(os.path.join("embedding_model", EMBEDDING_NAME), 'wb')
    pkl.dump(model, file)


max_sentence_length = 40
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
        x, t = embed_to_tensor(x_batches[i], model, count, total)

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
            x, t, _ = embed_to_tensor(test_x_batches[i], model, count, total)

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

