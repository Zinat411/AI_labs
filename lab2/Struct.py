from random import randint

class Struct:
    def __init__(self, str, fitness):
        self.str = str
        self.fitness = fitness
        self.age = 0
        self.permut = []
        self.score = 0
        self.species = -1
        self.centroid = -1

    def getString(self):
        return self.str

    def getFitness(self):
        return self.fitness

    def setString(self, string):
        self.str = string

    def setFitness(self, fitness):
        self.fitness = fitness