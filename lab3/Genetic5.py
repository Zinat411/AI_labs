import math
import sys

import numpy
import numpy as np

from Arguments import *
from Struct import *
import random
import math
from numpy.random import choice
from Heuristic import *
class Genetic5:
    def __init__(self, args,cvrp, stop):
        self.args = args
        self.cvrp=cvrp
        self.tsize = self.cvrp.Dimension
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)
        self.population = []
        self.buffer = []
        self.stop = stop
    def init_population(self): #create popsize citizens
        for i in range(len(self.cvrp.Cities)):
             str1 = get_best_neighbor(self.cvrp, len(self.cvrp.Cities))
             gene = Struct(str1, 0)
             self.population.append(gene)
             str2 = get_best_neighbor(self.cvrp, len(self.cvrp.Cities))
             gene2 = Struct(str2, 0)
             self.buffer.append(gene2)


    def gastart(self):
        fitlst = []
        check = 0
        final_best = float('inf')
        self.init_population()
        for i in range(self.args.maxiter):
            #for gene in self.population:
            self.calcfitness()
            self.sort_by_fitness(self.population)
            self.print_best(self.population)
            fitlst.append(self.population[0].fitness)
            #if self.population[0].getFitness() == 0:
            if check == self.stop or self.population[0].fitness == 0:
                print()
                print("Best string: " + str(self.population[0].str))
                print(f'found in {i} iterations out of {self.args.maxiter}')
                break
            best = self.population[0].getString()[:]
            best_fitness = self.population[0].fitness
            if final_best == best_fitness:
                check += 1
            if best_fitness < final_best:
                final_best = best_fitness
                check = 1
            self.mate(self.population, self.buffer)
            self.population, self.buffer = self.buffer, self.population
            self.cvrp.best_tour = best
            self.cvrp.best_cost = best_fitness
        return fitlst

    def calcfitness(self):
        fitness = 0
        for gene in self.population:
            fitness = self.cvrp.tour_cost_veh(gene.str)
            gene.fitness = fitness
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
        self.population.sort(key=lambda i: i.fitness)


    def elitism(self, problem):
        y = 0
        i = 0
        while i < problem.esize + y:
             if i == problem.args.GA_POPSIZE:
                   break
             if problem.population[i].getAge() > problem.args.AGE_MAX:
                   i += 1
                   y += 1
                   continue
             problem.nextPopulation.append(problem.population[i])
             i += 1


    def mate(self, population: list[Struct], buffer: list[Struct]):
        #self.elitism(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            gene =[]
            for j in range(int(self.tsize)):
                if self.population[i1].str[j-1]<self.tsize:
                   gene.append(self.population[i1].str[j-1])
                else:
                    gene.append(self.population[i2].str[j-1])
            self.buffer.append(Struct(gene, 0))
            #if random.random() < self.args.GA_MUTATION:
                 #self.mutate(self.buffer[i-1])

    def mutate(self, member: Struct):
        ipos = randint(0, self.tsize - 1)
        jpos = randint(0, self.tsize - 1)
        temp=member.str[ipos]
        member.str[ipos]=member.str[jpos]
        member.str[jpos]=temp
        # str1 = member.str[:ipos] + chr((ord(member.str[ipos]) + delta) % 122) + member.str[ipos + 1:]
        # member.str = str1
        #test

    def print_best(self, gav: list[Struct]):
        print('Best: ', self.population[0].str, '(', str(self.population[0].fitness), ')')

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
















