import random
class Var:
    def __init__(self, maxiter,popsize,eliteRate, mutationRate,):
        self.maxiter=maxiter
        self.GA_POPSIZE = popsize
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATION = mutationRate * random.random()


