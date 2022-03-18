import random
from enum import Enum
MIN = 32
ENTRIES = []

class Var:
    def __init__(self, popsize, maxIter, eliteRate, mutationRate, targetString, cross_type,nqueens=8,tournamentK=500,
                 numBins=3,weightarr=[12,10,2,4,8,34,12,87,23,33],binsize=[30,40,50],binnum=10):
        self.GA_POPSIZE = popsize
        self.GA_TARGET = targetString
        self.GA_MAXITER = maxIter
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATIONRATE = mutationRate
        self.GA_MUTATION = mutationRate * random.random()
        self.CROSS_TYPE = cross_type
        self.nqueens = nqueens
        self.tournamentK = tournamentK
        self.numBins = numBins
        self.weightarr = weightarr
        self.binsize = binsize
        self.binnum = binnum


