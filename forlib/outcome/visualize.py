from matplotlib import pyplot as plt


class PieChart:
    def __init__(self, data, label):
        self.data = data
        self.label = label
        self.__show()

    def __show(self):
        plt.pie(self.data, labels=self.label)
        plt.show()


class Timeline:
    def __init__(self, data):
        for i in range(0, len(data)):
            artifact1 = data[i]
            x = artifact1["time"]
            y = artifact1["num"]
            plt.plot(x, y)
            plt.xlabel('Time')
            plt.ylabel('Num')
        plt.show()
