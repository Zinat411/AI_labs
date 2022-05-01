import random
class Var:
    def __init__(self, maxiter,lastN,popsize,eliteRate, mutationRate,):
        self.maxiter=maxiter
        self.lastN=lastN
        self.GA_POPSIZE = popsize
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATION = mutationRate * random.random()


