import random
from enum import Enum
MIN = 32
ENTRIES = []

class Var:
    def __init__(self, popsize, maxIter, eliteRate, mutationRate, targetString, cross_type,nqueens=8,tournamentK=500):
        self.GA_POPSIZE = popsize
        self.GA_TARGET = targetString
        self.GA_MAXITER = maxIter
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATIONRATE = mutationRate
        self.GA_MUTATION = mutationRate * random.random()
        self.CROSS_TYPE = cross_type
        self.nqueens = nqueens
        self.tournamentK = tournamentK


