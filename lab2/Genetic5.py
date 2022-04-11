import math
import sys

import numpy
import numpy as np

from Arguments import *
from Struct import *
from Functions import  *
from random import randint, random, randrange
import math
from numpy.random import choice

class Genetic5:
    def __init__(self, args):
        self.args = args
        self.tsize = len(self.args.GA_TARGET)
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)

    def init_population(self, population: list, buffer: list): #create popsize citizens
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
        flag = 0
        temp = []
        while len(temp) < self.esize:
            if is_age(population[flag]) & flag < self.args.GA_POPSIZE:
                temp.append(population[flag])
                flag += 1
            else:
                flag += 1
        #temp = population[:self.esize].copy()
        buffer[:self.esize] = temp
        for i in range(self.esize):
            buffer[i].age += 1

    def mutate(self, member: Struct):
        ipos = randint(0, self.tsize - 1)
        delta = randint(0, 90) + 32
        str1 = member.str[:ipos] + chr((ord(member.str[ipos]) + delta) % 122) + member.str[ipos + 1:]
        member.str = str1

    def mate(self, population: list[Struct], buffer: list[Struct]):
        self.elitism(population, buffer)
        # y = logistic_decay(self.args.GA_POPSIZE)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = randint(0, (self.args.GA_POPSIZE/2) - 1)
           #i1 = self.RWS(population, buffer)[0]
           #i2 = self.RWS(population, buffer)[0]
           # i1 = self.tournamentSelection(population)
           # i2 = self.tournamentSelection(population)
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
            # min = 0.25
            # if y[i] < min:
            #     y[i] = min
            # if random() < y[i] * random():
            #     # adding the trigered hyper mutation condition if it drops down the min limit
            #     self.mutate(buffer[i])



    def print_best(self, gav: list[Struct]):
        print('Best: ', gav[0].str, '(', str(gav[0].fitness), ')')

    def swap(self, population: list[Struct], buffer: list[Struct]):
        population, buffer = buffer, population

    def roulette_spin(self, population: list[Struct], numberofwinners=1):
        # Given a list of fitnesses, returns the result of the roulette spin where
        # probability of choosing individual i = f(i)/sum(fitnesses)
        fitnesses: list[int] = []
        counter = 0
        max=0
        for pop in population:
            fitnesses.append(pop.fitness)
            if pop.fitness>max:
                max=pop.fitness
            counter += 1
        fitness_sum = sum(fitnesses)
        avg = self.calc_avg_fitness(population)
        sd = self.calc_SD(population, avg)

        probabilities = [fitness / fitness_sum for fitness in fitnesses]
        s=np.random.choice(len(fitnesses), numberofwinners, probabilities)
        return s, probabilities[s]

    def selection_pressure(self, population, prop):
        avg = self.calc_avg_fitness(population)
        count_avg = 0
        for pop in population:
            if pop.fitness - avg < abs(2.5):
                count_avg += 1
        avg_members = count_avg / self.args.GA_POPSIZE
        print("selection pressure is:", prop / avg_members)

    def RWS(self, population, buffer, f=-1):
        # Return num_winners RWS Selections
        selection, prop = self.roulette_spin(population)
        self.selection_pressure(population, prop)
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

    def randomwalk(self,intensity: int, population: list,subpop:int,h:int):
        counter=-1
        for pop in population:
            counter+=1

            for i in range(intensity):
                tempstr = pop.str
                for j in range(self.tsize):
                    if(j%h==0):
                        x = randint(0, 1)
                        tempstr = tempstr[:j] + chr((ord(tempstr[j])+x)) + tempstr[j + 1:]

                if (tempstr == self.args.GA_TARGET and pop.fitness>1):
                    pop.fitness = pop.fitness-1
                    break
            if(counter>=subpop):
                break

    def hillclimning(self,population,intensity,subpop,steepest:bool,h):
        counter = -1
        for pop in population:
            counter += 1
            for i in range(intensity):
                tempstr = pop.str
                bestfit = pop.fitness
                for j in range(self.tsize):
                    if (j % h == 0):
                        x = randint(0, 1)
                        tempstr = tempstr[:j] + chr((ord(tempstr[j]) + x)) + tempstr[j + 1:]
                        for k in range(self.tsize):
                            fitness = fitness + abs(ord(tempstr[k]) - ord(self.args.GA_TARGET[k]))

                        if(fitness<bestfit):
                            bestfit=fitness
                            pop.str=tempstr
                            pop.fitness=bestfit
                            if steepest:
                                break

                if (tempstr == self.args.GA_TARGET and pop.fitness > 1):
                    pop.fitness = pop.fitness - 1
                    break
            if (counter >= subpop):
                break


    def kgene(self,population: list[Struct],buffer,k):

        for i in range(self.esize, self.args.GA_POPSIZE):
            start = 0
            str=""
            for j in range(k):
                if j==k:
                    i1 = randint(0, (self.args.GA_POPSIZE / 2) - 1)
                    str = population[i].str[start:self.tsize]
                    start += k
                i1 = randint(0, (self.args.GA_POPSIZE / 2) - 1)
                str=population[i].str[start:(start+self.tsize/k)]
                start+=k

            buffer[i]=Struct(str,0)
            if random() < self.args.GA_MUTATION:
                self.mutate(buffer[i])

    def immigrants(self, buffer):
        index = 0
        for i in range(self.args.GA_POPSIZE- self.esize, self.args.GA_POPSIZE):
            buffer[i] = buffer[index]
            index += 1
            if randrange(sys.maxsize) < sys.maxsize:
                self.mutate(buffer[i])