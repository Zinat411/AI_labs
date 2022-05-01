import math
import sys

import numpy
import numpy as np

from Arguments import *
from Struct import *
import random
import math
from numpy.random import choice

class Genetic5:
    def __init__(self, args,cvrp):
        self.args = args
        self.cvrp=cvrp
        self.tsize = self.cvrp.Dimension
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)

    def init_population(self, population: list, buffer: list): #create popsize citizens
        for i in range(self.args.GA_POPSIZE):
             str1 = []
             fitness1 = 0
             best=list(range(1, self.cvrp.Dimension + 1))
             random.shuffle(best)
             structGA = Struct(best, fitness1)
             population.append(structGA)



    def calcfitness(self,path):
        fitness = 0
        i=0
        trucksnum=1
        Capacity = self.cvrp.Capacity

        fitness += self.cvrp.Distance_mat()[path[i+1]-1][0] #cost paid so far
        Capacity -= self.cvrp.Cities[path[i] - 1].demand #Capacity left


        while i < (self.cvrp.Dimension-2):
            x = path[i]
            y = path[i + 1]
            # print(x," coor ",y)
            if self.cvrp.Cities[y - 1].demand <= Capacity:
                cost = self.cvrp.Distance_mat()[x-1][y-1]
                Capacity -= self.cvrp.Cities[y - 1].demand
                fitness += cost
            else:
                fitness += self.cvrp.Distance_mat()[x-1][0]
                Capacity = self.cvrp.Capacity
                trucksnum += 1
                fitness += self.cvrp.Distance_mat()[y-1][0]
                Capacity -= self.cvrp.Cities[y - 1].demand
            i += 1

        fitness += self.cvrp.Distance_mat()[path[i]-1][0]
        return fitness

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
        flag = 0
        temp = []

        buffer[:self.esize] = temp


    def mate(self, population: list[Struct], buffer: list[Struct]):
        self.elitism(population, buffer)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)
           # i1 = self.RWS(population, buffer)[0]
           # i2 = self.RWS(population, buffer)[0]
           # i1 = self.tournamentSelection(population)
           # i2 = self.tournamentSelection(population)
            spos = randint(0, self.tsize - 1)

            gene =[]
            for j in range(int(self.tsize)):
                if population[i1].str[j-1]<self.tsize:
                   gene.append(population[i1].str[j-1])
                else:
                          gene.append(population[i2].str[j-1])

            buffer.append(Struct(gene, 0))
        # if random.random() < self.args.GA_MUTATION:
        #     self.mutate(buffer[i-1])

    def mutate(self, member: Struct):
        ipos = randint(0, self.tsize - 1)
        jpos = randint(0, self.tsize - 1)
        temp=member.str[ipos]
        member.str[ipos]=member.str[jpos]
        member.str[jpos]=temp
        # str1 = member.str[:ipos] + chr((ord(member.str[ipos]) + delta) % 122) + member.str[ipos + 1:]
        # member.str = str1

    def print_best(self, gav: list[Struct]):
        print('Best: ', gav[0].str, '(', str(gav[0].fitness), ')')

    def swap(self, population: list[Struct], buffer: list[Struct]):
        population, buffer = buffer, population

    def roulette_spin(self, population: list[Struct], numberofwinners=1):
        # Given a list of fitnesses, returns the result of the roulette spin where
        # probability of choosing individual i = f(i)/sum(fitnesses)
        fitnesses: list[int] = []
        counter = 0
        for pop in population:
            fitnesses.append(pop.fitness)
            counter += 1
        fitness_sum = sum(fitnesses)
        probabilities = [fitness / fitness_sum for fitness in fitnesses]
        return np.random.choice(len(fitnesses), numberofwinners, probabilities)

    def RWS(self, population, buffer, f=-1):
        # Return num_winners RWS Selections
        selection = self.roulette_spin(population)
        return selection

    def sigmascaling(self, population: list[Struct], i: int):
        avg = self.calc_avg_fitness(population)
        sd = self.calc_SD(population, avg)
        return 1 + (population[i].fitness - avg) / 2 * sd

    def SUS(self, population, esize):
        parent = self.args.GA_POPSIZE - esize
        fitness = [-1]
        max_fit = max(gene.fitness for gene in population)
        for i in range(len(population)):
            fitness.append(max_fit - population[i].fintess)
        fitness = numpy.array(fitness)
        total1 = fitness.total()
        total2 = total1[-1]
        forward = int(total2 / parent)
        begin = random.randrange(forward)
        selected_gene = np.arange(begin, total2, forward)
        selected_pop = np.searchsorted(total1, selected_gene)
        return [population[gene] for gene in selected_pop]


    def tournamentSelection(self, population):
        best = None
        index: int
        for i in range(self.args.tournamentK):
            person = population[randint(0, len(population) - 1)]
            if best is None:
                best = person
                index = i
            elif best.fitness > person.fitness:
                best = person
                index = i
        return index
















