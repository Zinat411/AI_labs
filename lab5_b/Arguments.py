import random
class Var:
    def __init__(self, maxiter,popsize,eliteRate, mutationRate,train_x,train_y,test_x,test_y):
        self.maxiter=maxiter
        self.GA_POPSIZE = popsize
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATION = mutationRate * random.random()
        self.train_x=train_x
        self.train_y=train_y
        self.test_x=test_x
        self.test_y=test_y


