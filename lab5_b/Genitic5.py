import math
from random import randint, random, randrange

from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier

from Agent import Agent
from numpy.random import choice, uniform

from Arguments import *
from NWAgent import NWAgent


class Genetic5:
    def __init__(self, args):
        self.best = None
        self.args = args
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)
        self.population = []
        self.parasites = []
        self.buffer = []

    def init_population(self):  # create popsize citizens

        for i in range(self.args.GA_POPSIZE):  # initialize the agents population
            array = []
            depth = random.randint(1, 10)
            for i in range(depth):
                array.append(random.randint(2, 200))
            if random.randint(0, 2) == 0:
                activate = 'relu'
            else:
                activate = 'tanh'

            agent = Agent(array, 0, NWAgent(depth, array, activate))
            self.population.append(agent)
        # ar=self.population[0].arr
        # f = 100
        # n = self.population[0].network
        # age = self.population[0].age
        # reg=self.population[0].reg
        # self.best=Agent(ar,f,n)
        # self. best.age=age
        # self. best.reg=reg

    def calc_fitness(self, population: list[Agent]):
        for i in range(self.args.GA_POPSIZE):
            mlp = MLPClassifier(hidden_layer_sizes=self.population[i].network.hidden, max_iter=30000,activation=self.population[i].network.activate, solver='adam', random_state=1)
            mlp.fit(self.args.train_x, self.args.train_y)
            conf = confusion_matrix(mlp.predict(self.args.test_x), self.args.test_y)
            sum = conf.sum()
            x = conf.trace()
            self.population[i].fitness = 1 - (x / sum)
            self.population[i].reg = 0

    def result(self, p1, p2):  # from lab4
        if ((p2 == 0 and p1 == 1) or (p2 == 1 and p1 == 2) or (p2 == 2 and p1 == 0)):
            return 1
        if ((p2 == 0 and p1 == 0) or (p2 == 1 and p1 == 1) or (p2 == 2 and p1 == 2)):
            return 0
        return -1

    def sort_by_fitness(self, population: list[Agent]):
        population.sort(key=lambda i: i.fitness)

    def elitism(self, population: list[Agent], buffer: list[Agent]):
        flag = 0
        temp = []
        while len(temp) < self.esize:
            temp.append(population[flag])
            flag += 1
        # temp = population[:self.esize].copy()
        self.population[:self.esize] = temp
        for i in range(self.esize):
            self.population[i].age += 1

    def mate(self):
        self.elitism(self.population, self.buffer)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = randint(0, (self.args.GA_POPSIZE / 2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE / 2) - 1)
            minsize = min(self.population[i1].network.depth, self.population[i2].network.depth)
            # i1 = self.RWS(population, buffer)[0]
            # i2 = self.RWS(population, buffer)[0]
            # i1 = self.tournamentSelection(population)
            # i2 = self.tournamentSelection(population)

            pos = random.randint(0, minsize)
            self.population[i].network.hidden = self.population[i1].network.hidden[0: pos] +self.population[i2].network.hidden[pos:]
            size=len(self.population[i].network.hidden)
            self.population[i].network.depth = size



    def commensalism(self):
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = i
            while i1 == i:
                i1 = randint(0, (self.args.GA_POPSIZE) - 1)

            res2 = [abs(num1 - num2) for num1, num2 in zip(self.best, self.population[i].arr)]
            res3 = [num * random.choice([-1, 1]) for num in res2]
            gene = [num + num2 for num, num2 in zip(self.population[i].arr, res3)]

            # gene=self.population[i].arr+randint(-1,1)*np.subtract(self.best,self.population[i].arr)
            loss = 0
            rounds = 0

            for par in self.parasites:
                par.newGame(len(gene))
                for k in range(len(gene)):
                    r = self.result(gene[k], par.nextMove())
                    rounds += r
                    par.storeMove(gene[k], r)
                if rounds < 0:
                    loss += 1
                rounds = 0

            if (loss < self.population[i].fitness):
                self.population[i] = Agent(gene, loss)

        self.paraisitsm()

    def paraisitsm(self):
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = i
            while i1 == i:
                i1 = randint(0, (self.args.GA_POPSIZE) - 1)
            pv = self.population[i].arr
            for j in range(len(self.population[i].arr)):
                if uniform(0, 1) < self.args.GA_MUTATION:
                    pv[j] = randint(0, 2)
            loss = 0
            rounds = 0

            for par in self.parasites:
                par.newGame(len(pv))
                for k in range(len(pv)):
                    r = self.result(pv[k], par.nextMove())
                    rounds += r
                    par.storeMove(pv[k], r)

                if rounds < 0:
                    loss += 1

                rounds = 0

            if (loss < self.population[i].fitness):
                self.population[i] = Agent(pv, loss)

    def print_best(self, gav: list[Agent]):
        print('Best: ', self.best.arr, '(', str(self.best.fitness), ')')

    def swap(self, population: list[Agent], buffer: list[Agent]):
        population, buffer = buffer, population

    def match(self):
        round = 0
        avg = 0
        sd = 0
        total = 0
        lst = []
        for bot in self.parasites:
            for i in range(10):
                bot.newGame(1000)
                for j in range(1000):
                    r = self.result(self.best[j], bot.nextMove())
                    round += r
                    bot.storeMove(self.best[j], r)

                lst.append(round)
                avg += round
                round = 0
            avg /= 10
            for i in range(10):
                total += abs(lst[i] - avg) ** 2
            sd = total / 10
            result = math.sqrt(sd)
            print("average against ", bot.getName(), " is: ", avg)
            print("sd against ", bot.getName(), "is: ", result)

    def tournament(self):
        round = 0
        results = {"Anti Flat Player": 0, "Copy Player": 0, "Freq Player": 0, "Flat Player": 0
            , "Foxtrot Player": 0, "Bruijn 81 Player": 0, "Pi Player": 0, "226 Player": 0
            , "Random Player": 0, "Rotating Player": 0, "Switching Player": 0, "Switch a Lot Player": 0, "us": 0}
        for par in self.parasites:
            for par2 in self.parasites:
                if par != par2:
                    par.newGame(1000)
                    par2.newGame(1000)
                    for i in range(1000):
                        a = par.nextMove()
                        b = par2.nextMove()
                        r = self.result(a, b)
                        round += r
                        par2.storeMove(a, r)
                        par2.storeMove(b, -r)
                    results[par.getName()] += round
                    results[par2.getName()] -= round

        for i in range(2):
            for par2 in self.parasites:
                par2.newGame(1000)
                for i in range(1000):
                    r = self.result(self.best[i], par2.nextMove())
                    round += r
                    par2.storeMove(self.best[i], r)
                results["us"] += round
                results[par2.getName()] -= round
        print(results)

    def reg(self):
        for i in range(self.args.GA_POPSIZE):
            mlp = MLPClassifier(hidden_layer_sizes=self.population[i].network.hidden, max_iter=30000,  activation=self.population[i].network.activate, solver='adam', random_state=1)
            counter = 0
            for j in range(len(mlp.coefs_)):
                for m in range(len(mlp.coefs_[j])):
                    counter += mlp.coefs_[j][m] * mlp.coefs_[j][m]

            calc = self.cacl_creg(self.population[i])
            self.population[i].reg = counter * (1 / calc) * (len(self.args.train_x))
