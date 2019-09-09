import copy

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import Conv2d, Linear, Dropout, AdaptiveMaxPool2d
import os
from news_sentiment.data_prep import *
import pickle as pkl
from torch.utils.tensorboard import SummaryWriter
from matplotlib import pyplot as plt


print("Loading model files...")

MODEL_PATH = "models\\cnn3.pkl"

EMBEDDING_NAME = "glove.twitter.27B.100d"
EMBEDDING = os.path.join("embeddings", EMBEDDING_NAME + ".txt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


try:
    file = open(os.path.join("embedding_model", EMBEDDING_NAME), 'rb')
    embed_model = pkl.load(file)
except FileNotFoundError:
    embed_model = load_glove_model(EMBEDDING)
    file = open(os.path.join("embedding_model", EMBEDDING_NAME), 'wb')
    pkl.dump(embed_model, file)


filter_size = 5
window_size = 2
padding = math.ceil((filter_size - 1)/2)
max_sentence_length = 100


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv = Conv2d(2, 512, (filter_size, 100), padding=(padding, 0))
        self.max_pooling = AdaptiveMaxPool2d((1, 1))
        self.fc1 = Linear(512, 256)
        self.fc2 = Linear(256, 3)
        self.dropout1 = Dropout(p=0.5)
        self.dropout2 = Dropout(p=0.5)

    def forward(self, x):
        x = self.dropout1(x)
        x = F.leaky_relu(self.conv(x))
        x = self.max_pooling(x)
        x = x.view(-1, 512)
        x = self.dropout2(x)
        x = F.leaky_relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=1)
        return x


label_names = ["negative, neutral, positive"]

data_path = "data\\acl-14-short-data"
train_path = os.path.join(data_path, "train.raw")
test_path = os.path.join(data_path, "test.raw")
mpqa_path = os.path.join("data", "mpqa.raw")

train_x, train_y, test_x, test_y = prep_mpqa_data(mpqa_path)


def train(net, train_x, train_y, test_x, test_y, num_epochs=15, batch_size=8, learning_rate=0.0001, write=True):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(net.parameters(), lr=learning_rate)

    if write:
        writer = SummaryWriter()

    x_batches = [train_x[i:i + batch_size] for i in range(0, batch_size * int(len(train_x) / batch_size), batch_size)]
    y_batches = [train_y[i:i + batch_size] for i in range(0, batch_size * int(len(train_y) / batch_size), batch_size)]
    test_x_batches = [test_x[i:i + batch_size] for i in
                      range(0, batch_size * int(len(test_x) / batch_size), batch_size)]
    test_y_batches = [test_y[i:i + batch_size] for i in
                      range(0, batch_size * int(len(test_y) / batch_size), batch_size)]

    running_loss = 0.0

    for epoch in range(num_epochs):
        running_loss = 0.0
        epoch_loss = 0.0
        c = list(zip(x_batches, y_batches))
        random.shuffle(c)
        x_batches, y_batches = zip(*c)
        epoch_correct = 0
        epoch_samples = 0
        correct = 0
        samples = 0
        for i in range(len(x_batches)):
            net.train()

            x = embed_to_tensor(x_batches[i], embed_model, max_sentence_length, window_size)

            labels = torch.tensor([j+1 for j in y_batches[i]], dtype=torch.long)

            optimizer.zero_grad()

            outputs = net(x)

            loss = criterion(outputs, labels)

            correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
            samples += batch_size

            epoch_correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
            epoch_samples += batch_size

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            epoch_loss += loss.item()

            if i % 100 == 99:
                print('[%d, %5d] loss: %.4f, acc: %.4f' %
                      (epoch + 1, i + 1, running_loss / 100, correct / samples))

                running_loss = 0.0
                correct = 0.0
                samples = 0.0

        running_loss = 0.0
        correct = 0
        samples = 0

        with torch.no_grad():
            net.eval()

            for i in range(len(test_x_batches)):
                x = embed_to_tensor(test_x_batches[i], embed_model, max_sentence_length, window_size)

                labels = torch.tensor([j + 1 for j in test_y_batches[i]], dtype=torch.long)

                outputs = net(x)

                samples += batch_size
                correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
                loss = criterion(outputs, labels)

                running_loss += loss.item()

        print('val_loss: %.4f, val_acc: %.4f' %
              (running_loss / len(test_x_batches), correct/samples), )
        if write:
            writer.add_scalar("loss/train", epoch_loss / len(x_batches), epoch)
            writer.add_scalar("loss/val", running_loss / len(test_x_batches), epoch)
            writer.add_scalar("accuracy/train", epoch_correct / epoch_samples, epoch)
            writer.add_scalar("accuracy/val", correct / samples, epoch)

        # writer.add_scalars("epoch loss", {"validation": running_loss / len(test_x_batches), "train": epoch_loss / len(x_batches)}, epoch)
        # writer.add_scalars("epoch accuracy", {"validation": correct / samples, "train": epoch_correct / epoch_samples}, epoch)

        torch.save(net.state_dict(), MODEL_PATH)

    print("finished training!")
    if write:
        writer.close()
    return running_loss/len(test_x_batches)


def forward_prop(x, net):
    if len(x) == 1:
        length = len(x[0][0]) + len(x[0][1]) - 1
    else:
        length = max_sentence_length
    inputs = embed_to_tensor(x, embed_model, length, window_size)
    outputs = net(inputs)
    return torch.argmax(outputs, dim=1).item() - 1


net = Net()


# if input("Load state_dict (y/n)").lower() == "y":
#     try:
#         net.load_state_dict(torch.load(MODEL_PATH))
#     except FileNotFoundError:
#         print("no valid model state_dicts")
# else:
#     train(net, train_x, train_y, test_x, test_y, num_epochs=10)


# for i, j in zip(test_x, test_y):
#     print(" ".join([j.decode() for j in i[0]]))
#     print(" ".join([j.decode() for j in i[1]]))
#     print(forward_prop([i]).item() - 1)
#     print(j)
#     print()


