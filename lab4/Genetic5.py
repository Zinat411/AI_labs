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

    def init_population(self): #create popsize citizens
          for i in range(1000):
              gene = Struct(uniform(0,10000,6), 0)
              self.parasites.append(gene)
          for j in range(self.args.GA_POPSIZE):
              nw = []
              for i in range(randrange(12,30)):
                  y = randrange(0, 6)
                  nw.append(y)
                  x=randrange(0,6)
                  while(x==y):
                      x = randrange(0, 6)
                  nw.append(x)
              gene = Struct(nw, 0)
              self.population.append(gene)




    def calc_fitness(self, population: list[Struct]):

        for test in self.parasites:
            fitness = 0
            for network in self.population:
              if self.sortByNetwork(network.arr,test.arr):
                  fitness+=1
            test.fitness=fitness/self.args.GA_POPSIZE

        for network in self.population:
            fitness = 0
            for test in self.parasites:
                if self.sortByNetwork(network.arr,test.arr):
                    fitness+=1
            network.fitness=(fitness/self.args.GA_POPSIZE)*len(network.arr)


    def sortByNetwork(self,network,test):
        test2=test
        for i in range(0,len(network)-1):

            temp=test2[network[i+1]]
            test2[network[i+1]]=test2[network[i]]
            test2[network[i]]=temp
            i += 1
        for i in range(len(test2)-1):
            if(test2[i]>test2[i+1]):
                return 1

        return 0


    def sort_by_fitness(self, population: list[Struct]):
        population.sort(key=lambda i: i.fitness)

    def print_sorted(self,network):
        for tests in self.parasites:
            test=tests.arr
            for i in range(0,len(network)-1):

                temp=test[network[i+1]]
                test[network[i+1]]=test[network[i]]
                test[network[i]]=temp
                i += 1
            print("sorted array: ",test)
    # def elitism(self, population: list[Struct], buffer: list[Struct]):
    #     flag = 0
    #     temp = []
    #     while len(temp) < self.esize:
    #         if is_age(population[flag]) & flag < self.args.GA_POPSIZE:
    #             temp.append(population[flag])
    #             flag += 1
    #         else:
    #             flag += 1
    #     #temp = population[:self.esize].copy()
    #     buffer[:self.esize] = temp
    #     for i in range(self.esize):
    #         buffer[i].age += 1

    def mate(self, population: list[Struct], buffer: list[Struct]):
        #self.elitism(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            gene =[]
            for j in range(0,min(len(population[i1].arr),len(population[i2].arr)),2):
                # if self.population[i1].str[j-1]<self.tsize:
                if(j%4==0):
                  self.population[i1].arr[j]=self.population[i2].arr[j]
                  self. population[i1].arr[j+1] =self. population[i2].arr[j+1]


            self.buffer.append(Struct(gene, 0))
            #if random.random() < self.args.GA_MUTATION:
                 #self.mutate(self.buffer[i-1])

    def mutate(self, member: Struct):
        ipos = randint(0, member.arr.len()-1,2)
        member[ipos]=randrange(0,6)
        member[ipos+1] = randrange(0, 6)
        # temp=member.str[ipos]
        # member.str[ipos]=member.str[jpos]
        # member.str[jpos]=temp
        # str1 = member.str[:ipos] + chr((ord(member.str[ipos]) + delta) % 122) + member.str[ipos + 1:]
        # member.str = str1
        #test



    def print_best(self, gav: list[Struct]):
        print('Best: ', gav[0].arr, '(', str(gav[0].fitness), ')')

    def swap(self, population: list[Struct], buffer: list[Struct]):
        population, buffer = buffer, population





