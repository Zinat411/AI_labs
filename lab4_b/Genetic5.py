import math
import math
import sys
from random import randint, random, randrange

# import numpy
import numpy as np

import Dummy
from Agent import Agent
from RoshamboPlayer import *
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

          for i in range(self.args.GA_POPSIZE): #initialize the agents population
              player = Agent(random.randint(0, 2))
              self.population.append(player)

          for j in range(10):

              self.parasites.append(Dummy.Pi)
              self.parasites.append(Dummy.Copy)
              self.parasites.append(Dummy.Flat)
              self.parasites.append(Dummy.Freq)
              self.parasites.append(Dummy.AntiFlat)
              self.parasites.append(Dummy.Bruijn81)
              self.parasites.append(Dummy.Foxtrot)
              self.parasites.append(Dummy.Play226)
              self.parasites.append(Dummy.RndPlayer)
              self.parasites.append(Dummy.Rotate)
              self.parasites.append(Dummy.Switch)
              self.parasites.append(Dummy.SwitchALot)


    def calc_fitness(self, population: list[Agent]):
        loss=0
        rounds=0
        for pop in self.population:
            for par in self.parasites:
                for i in range(len(pop.arr)):
                    if(self.beats(pop.arr[i],par.arr[i])):
                       rounds+=1
                if rounds<500:
                    loss+=1
                rounds=0
            pop.fitness=loss
            loss=0

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

            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)

            gene = []
            for j in range(len(self.population[i1].arr)):
                x =randint(0, sys.maxsize) % 2
                if x == 0:
                    gene.append(self.population[i1].arr[j])
                else:
                    gene.append(self.population[i2].arr[j])
            self.population[i] = Agent(gene, 0)
            if random.random() < self.args.GA_MUTATION:
                self.mutate(self.population[i])

    def mutate(self, member: Agent):
        ipos = randint(0, self.tsize - 1)
        x=member.arr[ipos]
        x+=1
        x%=3
        del member.arr[ipos]
        member.arr.insert(ipos,x)

    def print_best(self, gav: list[Agent]):
        print('Best: ', gav[0].arr, '(', str(gav[0].fitness), ')')



    def swap(self, population: list[Agent], buffer: list[Agent]):
        population, buffer = buffer, population


