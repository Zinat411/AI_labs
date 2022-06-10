import math
import math
import sys
from random import randint, random, randrange

# import numpy
import numpy as np

import Dummy
from Agent import Agent
from RoshamboPlayer import *
from numpy.random import choice, uniform

from Arguments import *


class Genetic5:
    def __init__(self, args):
        self.args = args
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)
        self.population = []
        self.parasites = []
        self.buffer = []
        self.best = []

    def init_population(self):  # create popsize citizens

        for i in range(self.args.GA_POPSIZE):  # initialize the agents population
            array = [random.randint(0, 2) for i in range(1000)]
            player = Agent(array, 0)
            self.population.append(player)

        for j in range(1):
            self.parasites.append(Dummy.AntiFlat())
            self.parasites.append(Dummy.Copy())
            self.parasites.append(Dummy.Freq())
            self.parasites.append(Dummy.Flat())
            self.parasites.append(Dummy.Foxtrot())
            self.parasites.append(Dummy.Bruijn81())
            self.parasites.append(Dummy.Pi())
            self.parasites.append(Dummy.Play226())
            self.parasites.append(Dummy.RndPlayer())
            self.parasites.append(Dummy.Rotate())
            self.parasites.append(Dummy.Switch())
            self.parasites.append(Dummy.SwitchALot())

    def calc_fitness(self, population: list[Agent]):
        loss = 0
        rounds = 0
        for pop in self.population:
            for par in self.parasites:
                par.newGame(len(pop.arr))
                for i in range(len(pop.arr)):
                    r = self.result(pop.arr[i], par.nextMove())
                    rounds += r
                    par.storeMove(pop.arr[i], r)
                if rounds < 0:
                    loss += 1
                rounds = 0
            pop.fitness = loss
            loss = 0

    def result(self, p1, p2):
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
            i1 = i
            # [num1 * num2 for num1, num2 in zip(a, b)]
            while i1 == i:
                i1 = randint(0, (self.args.GA_POPSIZE) - 1)
            bf1 = randint(1, 2)
            bf2 = randint(1, 2)
            # mv=np.add(self.population[i].arr,self.population[i1].arr)
            mv = [num1 + num2 for num1, num2 in zip(self.population[i].arr, self.population[i1].arr)]
            # mv=np.divide(mv,2)
            res = [int(num1 / 2) for num1 in mv]
            mv = res
            mv2 = mv
            res = [num * bf1 for num in mv]
            res2 = [abs(num1 - num2) for num1, num2 in zip(self.best, res)]
            res3 = [int(num * uniform(0, 1)) for num in res2]
            gene = [num + num2 for num, num2 in zip(self.population[i].arr, res3)]
            mv = mv2
            res = [num * bf2 for num in mv]
            res2 = [abs(num1 - num2) for num1, num2 in zip(self.best, res)]
            res3 = [int(num * uniform(0, 1)) for num in res2]
            gene2 = [num + num2 for num, num2 in zip(self.population[i1].arr, res3)]

            # gene=self.population[i].arr+np.multiply(randint(0,1),(np.subtract(self.best,np.multiply(mv,bf1))))
            # print(gene)

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
            loss = 0
            rounds = 0
            for par in self.parasites:
                par.newGame(len(gene2))
                for k in range(len(gene2)):
                    r = self.result(gene2[k], par.nextMove())
                    rounds += r
                    par.storeMove(gene2[k], r)
                if rounds < 0:
                    loss += 1
                rounds = 0

            if (loss < self.population[i1].fitness):
                self.population[i1] = Agent(gene2, loss)
        self.commensalism()

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
        print('Best: ', gav[0].arr, '(', str(gav[0].fitness), ')')

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
