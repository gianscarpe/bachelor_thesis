from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import Plotter
import time

accuracyPlotter = Plotter.Plotter(['Train_Accuracy'], 'Accuracy')
lossPlotter = Plotter.Plotter(['Training_Loss', 'Test_Loss'], 'Loss')
testAccPlotter = Plotter.Plotter(['Accuracy'], 'Test_Accuracy')
testLossPlotter = Plotter.Plotter(['Loss'], 'Test_Loss')




# Training settings
parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                    help='input batch size for training (default: 64)')
parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                    help='input batch size for testing (default: 1000)')
parser.add_argument('--epochs', type=int, default=50, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--start_epoch', type=int, default=1, metavar='N',
                    help='starting epoch')
parser.add_argument('--lr', type=float, default=0.01, metavar='LR',
                    help='learning rate (default: 0.01)')
parser.add_argument('--momentum', type=float, default=0.5, metavar='M',
                    help='SGD momentum (default: 0.5)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='disables CUDA training')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
parser.add_argument('--resume_weights', type=str, default='checkpoint.pth.tar', metavar='S',
                    help='Checkpoint')



args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()

torch.manual_seed(args.seed)
if args.cuda:
    torch.cuda.manual_seed(args.seed)


kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}
train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=True, download=True,
                   transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=args.batch_size, shuffle=True, **kwargs)
test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('../data', train=False, transform=transforms.Compose([
                       transforms.ToTensor(),
                       transforms.Normalize((0.1307,), (0.3081,))
                   ])),
    batch_size=args.test_batch_size, shuffle=True, **kwargs)


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.bn1 = nn.BatchNorm2d(10)
	self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
	self.bn2 = nn.BatchNorm2d(20)
	self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 150)
        self.fc2 = nn.Linear(150, 50)
        self.fc3 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.bn1(self.conv1(x)), 2))
        x = F.relu(F.max_pool2d( self.conv2_drop( self.bn2( self.conv2(x) ) ), 2 ))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
	x = F.dropout(x, training = self.training)
	x = self.fc3(x)
	return F.log_softmax(x, dim=1)

model = Net()
if args.cuda:
    model.cuda()

optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones = [31, 51], gamma = 0.1)

def train(epoch):
    model.train()
    average_time = 0
    tot_loss = 0
    for batch_idx, (data, target) in enumerate(train_loader):
        batch_time = time.time()
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        # Measure elapsed time
        batch_time = time.time() - batch_time
        # Accumulate over batch
        average_time += batch_time

        # ### Keep track of metric every batch
        # Accuracy Metric
        outputs = model(data)
        prediction = outputs.data.max(1)[1]   # first column has actual prob.
        accuracy = 100. * prediction.eq(target.data).sum() / (args.batch_size)

        tot_loss += loss.data[0]
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}, Accuracy: {:.4f}, Batch time: {:f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.data[0], accuracy, average_time/args.log_interval))
            global lossPlotter
    return tot_loss / len(train_loader)

def test():
    model.eval()
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        if args.cuda:
            data, target = data.cuda(), target.cuda()
        data, target = Variable(data, volatile=True), Variable(target)
        output = model(data)
        test_loss += F.nll_loss(output, target, size_average=False).data[0] # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1] # get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).long().cpu().sum()

    test_loss /= len(test_loader.dataset)
    accuracy = 100. * correct / len(test_loader.dataset)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),accuracy))
    global testAccPlotter
    testAccPlotter.plot(accuracy)
    global testLossPlotter
    testLossPlotter.plot(test_loss)
    return (accuracy, test_loss)

def save_checkpoint(state, filename=args.resume_weights):
        print ("=> Saving a new best")
        torch.save(state, filename)  # save checkpoint


for epoch in range(args.start_epoch, args.epochs + 1):
    scheduler.step()
    print ("Learning rate for this epoch: {}".format(scheduler.get_lr()))
    train_loss = train(epoch)
    (accuracy, test_loss) = test()
    lossPlotter.plot([train_loss, test_loss])
    save_checkpoint({
        'epoch': args.start_epoch + epoch + 1,
        'state_dict': model.state_dict(),
        'best_accuracy': accuracy,
        'learning_rate' : 0.1})
