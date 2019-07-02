import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import Conv2d, Linear, Dropout, MaxPool2d
import os
from data_prep import *
import pickle as pkl

EMBEDDING_NAME = "glove.twitter.27B.100d"
EMBEDDING = os.path.join("embeddings", EMBEDDING_NAME + ".txt")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

count = list()
count.append(0)

total = list()
total.append(0)


try:
    file = open(os.path.join("embedding_model", EMBEDDING_NAME), 'rb')
    model = pkl.load(file)
except FileNotFoundError:
    model = load_glove_model(EMBEDDING)
    file = open(os.path.join("embedding_model", EMBEDDING_NAME), 'wb')
    pkl.dump(model, file)


filter_size = 5
window_size = 2
padding = math.ceil((filter_size - 1)/2)
max_sentence_length = 50


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv = Conv2d(2, 512, (filter_size, 100), padding=(padding, 0))
        self.max_pooling = MaxPool2d((max_sentence_length, 100))
        self.fc1 = Linear(512, 256)
        self.fc2 = Linear(256, 3)
        self.dropout1 = Dropout(p=0.5)
        self.dropout2 = Dropout(p=0.5)

    def forward(self, x):
        x = self.dropout1(x)
        x = F.relu(self.conv(x))
        x = self.max_pooling(x)
        x = x.view(batch_size, 512)
        x = self.dropout2(x)
        x = F.relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=1)
        return x


net = Net()
num_epochs = 50
lr = 0.0001
batch_size = 8
label_names = ["negative, neutral, positive"]

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr=lr, weight_decay=0.01)
# scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, 5600, eta_min=0.0001)

data_path = "data\\acl-14-short-data"
train_path = os.path.join(data_path, "train.raw")
test_path = os.path.join(data_path, "test.raw")

train_x, train_y, test_x, test_y = prep_twitter_data(train_path, test_path)

x_batches = [train_x[i:i+batch_size] for i in range(0, batch_size * int(len(train_x)/batch_size), batch_size)]
y_batches = [train_y[i:i+batch_size] for i in range(0, batch_size * int(len(train_y)/batch_size), batch_size)]


for epoch in range(num_epochs):
    running_loss = 0.0
    c = list(zip(x_batches, y_batches))
    random.shuffle(c)
    x_batches, y_batches = zip(*c)
    correct = 0
    samples = 0
    for i in range(len(x_batches)):
        net.train()

        # scheduler.step()

        x = embed_to_tensor(x_batches[i], model, max_sentence_length, window_size, count, total)

        labels = torch.tensor([j+1 for j in y_batches[i]], dtype=torch.long)

        optimizer.zero_grad()

        outputs = net(x)

        loss = criterion(outputs, labels)

        correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
        samples += batch_size

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        if i % 100 == 99:
            print('[%d, %5d] loss: %.4f, acc: %.4f' %
                  (epoch + 1, i + 1, running_loss / 100, correct / samples))
            running_loss = 0.0

    # scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, 5600)

    running_loss = 0.0
    correct = 0
    samples = 0

    with torch.no_grad():
        net.eval()
        test_x_batches = [test_x[i:i + batch_size] for i in
                     range(0, batch_size * int(len(test_x) / batch_size), batch_size)]
        test_y_batches = [test_y[i:i + batch_size] for i in
                     range(0, batch_size * int(len(test_y) / batch_size), batch_size)]

        for i in range(len(test_x_batches)):
            x = embed_to_tensor(test_x_batches[i], model, max_sentence_length, window_size, count, total)

            labels = torch.tensor([j + 1 for j in test_y_batches[i]], dtype=torch.long)

            outputs = net(x)

            samples += batch_size
            correct += sum(torch.eq(torch.argmax(outputs, dim=1), labels).cpu().detach().numpy())
            loss = criterion(outputs, labels)

            running_loss += loss.item()

    print('val_loss: %.4f, val_acc: %.4f' %
          (running_loss / len(test_x_batches), correct/samples), )
    running_loss = 0.0

    print("finished training!")


r = int(np.random.uniform()*10)
x, _, t = embed_to_tensor(test_x_batches[r], model, max_sentence_length, window_size,4 count, total)
x = x.transpose(0, 1)[None, :, :, :].transpose(0, 1)
out = net(x, t)
for i in range(len(test_x_batches[r])):
    print(str(test_x_batches[r][i]) + "\n" + str(out[i]))
