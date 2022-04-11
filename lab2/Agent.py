from random import randint

class Agent:
    def __init__(self, str, fitness,learningfit,learningalgo):
        self.str = str
        self.fitness = fitness
        self.age = 0
        self.permut = []
        self.learningfit=learningfit
        self.learningalgo=learningalgo

    def getString(self):
        return self.str

    def getFitness(self):
        return self.fitness

    def setString(self, string):
        self.str = string

    def setFitness(self, fitness):
        self.fitness = fitness

