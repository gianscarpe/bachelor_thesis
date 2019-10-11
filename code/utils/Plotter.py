import visdom
import torch

class Plotter():
    def __init__(self, legend, winTitle):
        self.plottedValues = []
        self.vis = visdom.Visdom()
        self.opts = {'legend' : legend, 'title' : winTitle}
        self.win = ""

    def reset_plottedValues(self):
        self.plottedValues = []

    def add_value_at(self, value, index):
        if (self.check_plottedValuesIndex(index)):
            self.plottedValues[index].append([torch.Tensor([value])])

    def add_value(self, value):
            self.plottedValues.append(torch.Tensor([value]))

    def check_plottedValuesIndex(self, index):
        return len(self.plottedValues) > index

    def add_plottedValuesArray(self):
        self.plottedValues.append([])
        return len(self.plottedValues)-1


    def plot(self, value):
        if not(isinstance(value, list) or isinstance(value, tuple)):
            value = [value]

        self.add_value(value)
        l = self.get_current_length()
        x = self.get_current_x(l, len(value))
        self.plot_impl(x, value)


    def get_current_length(self):
        return len(self.plottedValues)

    def get_current_x(self, xvalue, ylength):
        x = []
        for i in range(ylength):
            x.append(xvalue)
        return x

    def plot_impl(self, x, y):
        if len(y) > 1:
            y = [y]
        if len(x) > 1:
            x = [x]

        if self.win == "":
            self.new_visdom_window(x, y)
        else:
            self.update_visdom_window(x, y)

    def new_visdom_window(self, x, y):
            self.win = self.vis.line(X=torch.Tensor(x), Y=torch.Tensor(y), opts=self.opts)

    def update_visdom_window(self, x, y):

        self.vis.line(X=torch.Tensor(x), Y=torch.Tensor(y), win = self.win, update='append')
