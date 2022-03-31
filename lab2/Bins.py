
class Bins:
    def __init__(self, arr, fitness):
        self.arr = arr
        self.fitness = fitness

    def getString(self):
        return self.arr

    def getFitness(self):
        return self.fitness

    def setString(self, arr):
        self.arr = arr

    def setFitness(self, fitness):
        self.fitness = fitness
