import math
import math
import sys
from random import randint, random, randrange

# import numpy
import numpy as np
from Struct import *
from numpy.random import choice,uniform

from Arguments import *


class Genetic5:
    def __init__(self, args):
        self.args = args
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)
        self.population = []
        self.parasites = []
        self.buffer = []
        self.nwsize=6
        self.minlength=12
        self.maxlength=20

    def init_population(self): #create popsize citizens
          for i in range(100):
              gene = Struct(np.random.randint(0,self.nwsize,self.nwsize), 0)
              self.parasites.append(gene)
          for j in range(self.args.GA_POPSIZE):
              nw = []
              for k in range(randrange(self.minlength, self.maxlength)):
                  y = randrange(0, self.nwsize)
                  nw.append(y)
                  x=randrange(0,self.nwsize)
                  while(x==y):
                      x = randrange(0, self.nwsize)
                  nw.append(x)
              gene = Struct(nw, 0)
              self.population.append(gene)

    def calc_fitness(self, population: list[Struct]):

        # for test in self.parasites:
        #     fitness = 0
        #     for network in self.population:
        #       if self.sortByNetwork(network.arr,test.arr):
        #           fitness+=1
        #     test.fitness=fitness/self.args.GA_POPSIZE

        for network in self.population:
            fitness = 0
            depth=len(network.arr)
            for test in self.parasites:
                if self.sortByNetwork(network.arr,test.arr):
                    fitness+=1
            network.fitness=(fitness/100)*depth

    def sortByNetwork(self,network,test):
        test2=[]
        for i in test:
            test2.append(i)
        for i in range(0,len(network)-1,2):
            if test2[network[i]]>test2[network[i+1]]:
                temp = test2[network[i + 1]]
                test2[network[i + 1]] = test2[network[i]]
                test2[network[i]] = temp
        for i in range(len(test2)-1):
            if(test2[i]>test2[i+1]):
                return True

        return False


    def sort_by_fitness(self, population: list[Struct]):
        population.sort(key=lambda i: i.fitness)

    def print_sorted(self,network):
        for tests in self.parasites:
            test=tests.arr
            test2 = []
            for i in test:
                test2.append(i)
            for i in range(0, len(network) - 1, 2):
                if test2[network[i]] > test2[network[i + 1]]:
                    temp = test2[network[i + 1]]
                    test2[network[i + 1]] = test2[network[i]]
                    test2[network[i]] = temp
            print("sorted array: ",test2)
    def elitism(self, population: list[Struct], buffer: list[Struct]):
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

            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)

            gene = []
            for j in range(min(len(self.population[i1].arr),len(self.population[i2].arr))):
                x =randint(0, sys.maxsize) % 2
                if x == 0:
                    gene.append(self.population[i1].arr[j])
                else:
                    gene.append(self.population[i2].arr[j])
            self.population[i] = Struct(gene, 0)
            if random.random() < self.args.GA_MUTATION:
                self.mutate(self.population[i])

    def mutate(self, member: Struct):
        ipos = randint(0,len( member.arr)-1)
        del member.arr[ipos]
        ipos = randint(0, len(member.arr) - 1)
        if ipos%2==1:
            ipos-=1
        y=randrange(0,self.nwsize)
        x = randrange(0, self.nwsize)
        while x==y:
            x = randrange(0, self.nwsize)

        member.arr.insert(ipos,x)
        member.arr.insert(ipos+1, y)


    def print_best(self, gav: list[Struct]):
        print('Best: ', gav[0].arr, '(', str(gav[0].fitness), ')')



    def swap(self, population: list[Struct], buffer: list[Struct]):
        population, buffer = buffer, population


