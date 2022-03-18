import random
import Struct
import sys
from Struct import Struct
import numpy as np

class NQueens:
    def __init__(self,args):
        self.args=args
        self.nqueens=args.nqueens


    def canQueenAttack(self,qR, qC, oR, oC):

        # If queen and the opponent are
        # in the same row
        if qR == oR:
            return True

        # If queen and the opponent are
        # in the same column
        if qC == oC:
            return True

        # If queen can attack diagonally
        if abs(qR - oR) == abs(qC - oC):
            return True

        # Opponent is safe
        return False

    def calc_fitness(self, population: list[Struct]):

        for i in range(self.args.GA_POPSIZE):
             fitness = self.nqueens
             counter=0
             for j in range(self.nqueens):
                 for x in range(self.nqueens):
                     if j!=x:
                      att=self.canQueenAttack((ord(population[i].str[j])-48),j+1,(ord(population[i].str[x])-48),(x+1))
                      if att:
                         counter = 1
                 if counter==0:
                      fitness-=1
             population[i].fitness = fitness

    def sort_by_fitness(self, population: list[Struct]):
        population.sort(key=lambda i: i.fitness)
    def elitism(self, population: list[Struct], buffer: list[Struct]):
        temp = population[:self.nqueens].copy()
        buffer[:self.nqueens] = temp
    def init_population(self, population: list, buffer: list): #create popsize citizens
        for i in range(self.args.GA_POPSIZE):
             str1 = ''
             fitness1 = 0
             for _ in range(self.nqueens):
                 str1 += chr(random.randrange(1,self.nqueens)+48)
             structGA = Struct(str1, fitness1)
             population[i] = structGA

    def mate(self, population: list[Struct], buffer: list[Struct]):
        self.elitism(population, buffer)
        for i in range(0, self.args.GA_POPSIZE):
            i1 = random.randint(0, (self.args.GA_POPSIZE/2) - 1)
            i2 = random.randint(0, (self.args.GA_POPSIZE/2) - 1)

            spos = random.randint(0, self.nqueens - 1)
            if (self.args.CROSS_TYPE == "Single"):
                buffer[i] = Struct(population[i1].str[0: spos] + population[i2].str[spos:], 0)
            if (self.args.CROSS_TYPE == "Two"):
                spos1 = random.randint(0, self.nqueens - 2)
                spos2 = random.randint(spos1 + 1, self.nqueens - 1)
                buffer[i] = Struct(
                    population[i1].str[0: spos1] + population[i2].str[spos1:spos2] + population[i1].str[spos2:], 0)
            if (self.args.CROSS_TYPE == "Uniform"):
                gene = ""
                for j in range(self.nqueens):
                    x = random.randint(0, sys.maxsize) % 2
                    if x == 0:
                        gene = gene + population[i1].str[j]
                    else:
                        gene = gene + population[i2].str[j]
                buffer[i] = Struct(gene, 0)
            if random.random() < self.args.GA_MUTATION:
                self.mutate(buffer[i])

    def print_best(self, gav: list[Struct]):
        print('Best: ', gav[0].str, '(', str(gav[0].fitness), ')')


    def swap(self, population: list[Struct], buffer: list[Struct]):
        population, buffer = buffer, population



    def mutate(self,member: Struct):
        pos=0;
        for num in member.str:
            if random.random() < 0.1:
              member.str =member.str[:pos]+ chr(random.randrange(self.nqueens)+48)+member.str[pos+1:]
            pos += 1
        return member







