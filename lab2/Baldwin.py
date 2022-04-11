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

class Baldwin:
    def __init__(self,args):
        self.args = args
        self.tsize = len(self.args.GA_TARGET)
        self.esize = int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)

    def init_population(self,population:list,buffer:list):
        for i in range(self.args.GA_POPSIZE):
            str1=""

            for j in range(self.tsize):
                x = randint(0, 3)
                if(x==0):
                    str1+='0'
                if(x==1):
                    str1+='1'
                if(x==2or x==3):
                    str1+='?'
            population[i]=Struct(str1,0)


    def calc_fitness(self,population):
        incorrect=0
        fixed=0
        tempstr=""
        for pop in population:
            pop.fitness = 1
            fixed += self.diff_letters(pop.str, self.args.GA_TARGET)
            for i in range(1000):
                tempstr=pop.str
                for j in range(self.tsize):
                    if(pop.str[j]=='?'):
                        x = randint(0, 1)
                        if (x == 0):
                            tempstr=tempstr[:j]+'0'+tempstr[j+1:]
                        if (x == 1):
                            tempstr=tempstr[:j]+'1'+tempstr[j+1:]
                incorrect += self.diff_letters(tempstr, self.args.GA_TARGET)
                if(tempstr==self.args.GA_TARGET):
                    pop.fitness=1+(19*(1000-i))/1000
                    break
                # incorrect+=self.diff_letters(tempstr,self.args.GA_TARGET)
        incorrectper=incorrect/(1000*self.tsize*self.args.GA_POPSIZE)
        correctper=1-incorrectper
        fixedper=1-(fixed/(self.tsize*self.args.GA_POPSIZE))
        print("incorrect position percentage:",incorrectper)
        print("correct position percentage:", correctper)
        print("fixed position percentage:", fixedper)
        return incorrectper,correctper,fixedper


    def diff_letters(self,a, b):
        return sum(a[i] != b[i] for i in range(len(a)))
    def sort_by_fitness(self, population: list[Struct]):
        population.sort(key=lambda i: i.fitness,reverse=True)
    def elitism(self, population: list[Struct], buffer: list[Struct]):
        flag = 0
        temp = []
        while len(temp) < self.esize:
            if is_age(population[flag]) & flag < self.args.GA_POPSIZE:
                temp.append(population[flag])
                flag += 1
            else:
                flag += 1
        # temp = population[:self.esize].copy()
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