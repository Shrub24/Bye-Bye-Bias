import copy

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import Conv2d, Linear, Dropout, AdaptiveMaxPool2d
import os
from data_prep import *
import pickle as pkl
from torch.utils.tensorboard import SummaryWriter
from transformers.modeling_bert import *
from transformers.tokenization_bert import BertTokenizer
import numpy

BATCH_SIZE = 4
MAX_LENGTH = 100


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.bert = BertModel.from_pretrained("bert-base-uncased")
        self.pool = AdaptiveMaxPool2d((1, None))
        self.fc1 = Linear(768, 256)
        self.fc2 = Linear(256, 3)
        self.dropout = Dropout(p=0.5)
        self.freeze_bert_weights()

    def forward(self, x, t):
        x = self.bert(x)[0]
        t = torch.unsqueeze(t, 2)
        x = torch.mul(x, t)
        x = self.dropout(x)
        x = self.pool(x)
        x = F.leaky_relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=2)
        return x

    def freeze_bert_weights(self):
        for param in self.bert.parameters():
            param.requires_grad = False

    def unfreeze_bert_weights(self):
        for param in self.bert.parameters():
            param.requires_grad = True


bertnet = Net()

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)


def bert_input_prep(x):
    prepped_input = list()
    for sample, i in x:
        prepped_sample = ['[CLS]'] + tokenizer.tokenize(sample)
        prepped_sample.extend(['[PAD]'] * (100 - len(prepped_sample)))
        target = tokenizer.tokenize(sample[i[0]: i[1]])
        indices = [(i, i+len(target)) for i in range(len(prepped_sample)) if prepped_sample[i:i+len(target)] == target][0]
        prepped_sample = tokenizer.convert_tokens_to_ids(prepped_sample)
        target = torch.zeros(len(prepped_sample))
        target[indices[0]: indices[1]] = torch.ones(indices[1] - indices[0])
        prepped_input.append((torch.tensor(prepped_sample), target))
    prepped_input = list(zip(*prepped_input))
    x = torch.stack(prepped_input[0])
    t = torch.stack(prepped_input[1])
    return x, t


print(bertnet(*bert_input_prep([("Hello I am Saurabh Jhanjee", (6, 7)), ("I am just kidding, I am not Saurabh!", (0, 1))])))