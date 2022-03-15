import math
import sys

from Arguments import *
from Struct import *
from random import randint, random, randrange
import math
from numpy.random import choice

class Genetic5:
    def __init__(self, args):
        self.args = args
        self.tsize = len(self.args.GA_TARGET)
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)

    def init_population(self, population: list, buffer: list):
        for i in range(self.args.GA_POPSIZE):
             str1 = ''
             fitness1 = 0
             for _ in range(self.tsize):
                 str1 += chr(randrange(0, 90) + 32)
             structGA = Struct(str1, fitness1)
             population[i] = structGA

    def calc_fitness(self, population: list[Struct]):

        for i in range(self.args.GA_POPSIZE):
            fitness = 0
            for j in range(self.tsize):
                fitness = fitness + abs(ord(population[i].str[j]) - ord(self.args.GA_TARGET[j]))
            population[i].fitness = fitness

    def calc_avg_fitness(self, population: list[Struct]):# this function calculates the average of the fitness
        totalfitness = 0
        avgfitness = 0
        for i in range(self.args.GA_POPSIZE):
            totalfitness += population[i].getFitness()
        avgfitness = totalfitness / self.args.GA_POPSIZE
        return avgfitness
    def calc_SD(self, population: list[Struct], avg):# this function calculates the standard deviation
        total = 0
        for i in range(self.args.GA_POPSIZE):
            total += abs(population[i].getFitness() - avg)**2
        sd = total / self.args.GA_POPSIZE
        result = math.sqrt(sd)
        return result

    def sort_by_fitness(self, population: list[Struct]):
        population.sort(key=lambda i: i.fitness)


    def elitism(self, population: list[Struct], buffer: list[Struct]):
        temp = population[:self.esize].copy()
        buffer[:self.esize] = temp

    def mutate(self, member: Struct):
        ipos = randint(0, self.tsize - 1)
        delta = randint(0, 90) + 32
        str1 = member.str[:ipos] + chr((ord(member.str[ipos]) + delta) % 122) + member.str[ipos + 1:]
        member.str = str1

    def mate(self, population: list[Struct], buffer: list[Struct]):
        self.elitism(population, buffer)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            spos = randint(0, self.tsize - 1)
            if(self.args.CROSS_TYPE == "Single"):
                buffer[i] = Struct(population[i1].str[0: spos] + population[i2].str[spos:], 0)
            if(self.args.CROSS_TYPE =="Two"):
                spos1 = randint(0, self.tsize - 2)
                spos2 = randint(spos1 + 1, self.tsize - 1)
                buffer[i] = Struct(population[i1].str[0: spos1] + population[i2].str[spos1:spos2] + population[i1].str[spos2:], 0)
            if(self.args.CROSS_TYPE == "Uniform"):
                gene = ""
                for j in range(self.tsize):
                    x =randint(0, sys.maxsize) % 2
                    if x == 0:
                        gene = gene + population[i1].str[j]
                    else:
                        gene = gene + population[i2].str[j]
                buffer[i] = Struct(gene, 0)
            if random() < self.args.GA_MUTATION:
                self.mutate(buffer[i])



    def print_best(self, gav: list[Struct]):
        print('Best: ', gav[0].str, '(', str(gav[0].fitness), ')')

    def swap(self, population: list[Struct], buffer: list[Struct]):
        population, buffer = buffer, population


















