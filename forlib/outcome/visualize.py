import errno
import os
from matplotlib import pyplot as plt


class PieChart:
    def __init__(self, data, name):
        self.data = data
        self.__name = name
        self.__show()

    def __show(self):
        plt.figure(3)
        plt.pie(self.data.values(), labels=self.data.keys())
        try:
            if not (os.path.isdir('result')):
                os.makedirs(os.path.join('result'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("fail to create folder")
                raise
        plt.savefig('./result/'+self.__name+'.png')


class Timeline:
    def __init__(self, data, file_name):
        keys = list(data.keys())
        values = list(data.values())
        plt.figure(2)
        plt.plot(keys, values)
        plt.xticks(rotation=90, fontsize=5)
        try:
            if not (os.path.isdir('result')):
                os.makedirs(os.path.join('result'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("fail to create folder")
                raise
        plt.savefig('./result/'+file_name+'.png')

class BarChart:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name
        self.__show()

    def __show(self):
        x = list(self.data.keys())
        y = list(self.data.values())
        plt.figure(figsize=(8, 7))
        plt.bar(x, y, width=0.5)
        plt.xticks(rotation=90, fontsize=8)

        try:
            if not (os.path.isdir('result')):
                os.makedirs(os.path.join('result'))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("fail to create folder")
                raise
        plt.savefig('./result/'+self.file_name+'.png', dpi=100)
