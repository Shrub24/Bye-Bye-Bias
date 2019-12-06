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
from transformers.modeling_bert import *
from transformers.tokenization_bert import BertTokenizer
import numpy

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BATCH_SIZE = 4
MAX_LENGTH = 100


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.pool = AdaptiveMaxPool2d((1, None))
        self.fc1 = Linear(768, 3)
        self.fc2 = Linear(256, 3)
        self.dropout = Dropout(p=0.25)
        self.freeze_bert_weights()

    def forward(self, x, t):
        x = self.bert(x)[0]
        t = torch.unsqueeze(t, 2)
        x = torch.mul(x, t)
        x = self.dropout(x)
        x = self.pool(x)
        x = torch.squeeze(x)
        x = F.softmax(self.fc1(x), dim=1)
        return x

    def freeze_bert_weights(self):
        for param in self.bert.parameters():
            param.requires_grad = False

    def unfreeze_bert_weights(self):
        for param in self.bert.parameters():
            param.requires_grad = True


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)


def bert_input_prep(x):
    prepped_input = list()
    for sample, i in x:
        sample = sample.replace("$T$", i)
        prepped_sample = ['[CLS]'] + tokenizer.tokenize(sample)
        prepped_sample.extend(['[PAD]'] * (100 - len(prepped_sample)))
        prepped_sample = prepped_sample[:100]
        target = tokenizer.tokenize(i)
        indices = [(i, i+len(target)) for i in range(len(prepped_sample)) if prepped_sample[i:i+len(target)] == target][0]
        prepped_sample = tokenizer.convert_tokens_to_ids(prepped_sample)
        target = torch.zeros(len(prepped_sample))
        target[indices[0]: indices[1]] = torch.ones(indices[1] - indices[0])
        prepped_input.append((torch.tensor(prepped_sample), target))
    prepped_input = list(zip(*prepped_input))
    x = torch.stack(prepped_input[0])
    t = torch.stack(prepped_input[1])
    return x, t


def train(net, train_x, train_y, test_x, test_y, num_epochs=5, batch_size=8, learning_rate=0.0002, write=True, save_path="models\\bert.pkl"):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(net.parameters(), lr=learning_rate)
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

            x, t = bert_input_prep(x_batches[i])
            x = x.to(device)
            t = t.to(device)

            labels = torch.tensor([j + 1 for j in y_batches[i]], dtype=torch.long).to(device)

            optimizer.zero_grad()

            outputs = net(x, t)

            loss = criterion(outputs, labels)

            correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
            samples += batch_size

            epoch_correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
            epoch_samples += batch_size

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            epoch_loss += loss.item()

            del x, t, labels, loss

            if i % 50 == 49:
                print('[%d, %5d] loss: %.4f, acc: %.4f' %
                      (epoch + 1, i + 1, running_loss / 50, correct / samples))

                running_loss = 0.0
                correct = 0.0
                samples = 0.0

        running_loss = 0.0
        correct = 0
        samples = 0

        with torch.no_grad():
            net.eval()

            for i in range(len(test_x_batches)):
                x, t = bert_input_prep(test_x_batches[i])
                x = x.to(device)
                t = t.to(device)

                labels = torch.tensor([j + 1 for j in test_y_batches[i]], dtype=torch.long).to(device)

                outputs = net(x, t)

                samples += batch_size
                correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
                loss = criterion(outputs, labels)

                running_loss += loss.item()

                del x, t, labels, loss

        print('val_loss: %.4f, val_acc: %.4f' %
              (running_loss / len(test_x_batches), correct / samples),)
        if write:
            writer.add_scalar("loss/train", epoch_loss / len(x_batches), epoch)
            writer.add_scalar("loss/val", running_loss / len(test_x_batches), epoch)
            writer.add_scalar("accuracy/train", epoch_correct / epoch_samples, epoch)
            writer.add_scalar("accuracy/val", correct / samples, epoch)

        torch.save(net.state_dict(), save_path)

    print("finished training!")
    if write:
        writer.close()
    return running_loss / len(test_x_batches)


def forward_prop(x, net):
    x, t = bert_input_prep(x)
    outputs = net(x, t)
    return torch.argmax(outputs, dim=1).item() - 1
