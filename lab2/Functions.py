from Genetic5 import *
from Arguments import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import itertools

def normalize(population, args1):# function that normalize the fitness values to be between 0 and 100
    max_fit = 0
    norm_fitness = [0] * args1.GA_POPSIZE
    for i in range(args1.GA_POPSIZE):# find the max value of fitness
        if population[i].fitness > max_fit:
            max_fit = population[i].fitness
    min_fit = max_fit
    for i in range(args1.GA_POPSIZE):# find the min value of fitness
        if population[i].fitness < min_fit:
            min_fit = population[i].fitness
    for i in range(args1.GA_POPSIZE):#this array stores the normalized value of the fitness
       norm_fitness[i] = math.floor(100 * (population[i].fitness - min_fit) / (max_fit - min_fit))
       #norm_fitness[i] = (100 * population[i].fitness) // max_fit
       #print("the norm fitness", norm_fitness[i])
    return norm_fitness

def histogram(norm_fitness, population: list[Struct], args1):
    x = [0] * 101
    for i in range(100):
        x[i] = i
    y = [0] * 101 # array that stores in each cell how many gens got this fitness value
    for i in range(args1.GA_POPSIZE):
        index = norm_fitness[i]
        y[index] += 1

    #for i in range(100):
        #print("Y is:", y[i])

    plt.scatter(x, y)
    for i in range(1,10):# split the graph to quantiles each one with the size of 10% of popsize
       plt.axvline(x=(norm_fitness[204*i]))

    #plt.rcParams.update({'figure.figsize': (10, 8), 'figure.dpi': 100})
    plt.title('The distribution of the genes fitnesses')
    plt.xlabel('Fitness')
    plt.ylabel('Num of genes')
    plt.show()
def bull_hits(population: list[Struct], args1): # this function implement bull heuristic that gives penalty of the fitness if the letter is not in the right place or if it doesn't exist
   for i in range(args1.GA_POPSIZE):
       new_fitness = 0
       tsize = len(args1.GA_TARGET)
       for j in range(tsize):
           if population[i].str[j] == args1.GA_TARGET[j]:# if the letter in the right place don't give penalty
              new_fitness += 0
           else:
              for k in range(j+1, tsize):
                  if population[i].str[j] == args1.GA_TARGET[k]:# if the letter somewhere in the string give it some penalty
                     new_fitness += 25
                     break
              new_fitness += 50 #if the letter dosen't exist in the target string give it heavy penalty
       population[i].fitness = new_fitness
def is_age(gene):#function to check if the gene in the appropriate range of age
    if 2 <= gene.age <= 30:
        return 1
    else:
        return 0

def pmx(perm1, perm2):
    str_size = len(perm1)
    pmx = randint(0, str_size-1)
    index1 = perm1[pmx]
    index2 = perm2[pmx]
    for i in range(str_size):
        if perm1[i] == index2:
            perm1[i], perm1[pmx] = index1, perm1[i]
    for i in range(str_size):
        if perm2[i] == index1:
            perm2[i], perm2[pmx] = index2, perm2[i]

    return [perm1, perm2]

def cx(perm1, perm2):
    size = len(perm1)
    child1 = Struct("", 0)
    child2 = Struct("", 0)
    for i in range(size):#initilize the permutation of each  child with -1
        child1.permut[i] = -1
        child2.permut[i] = -1
    first = randint(1, 2)#choose randomly(or from the first parent or the second)  the first chromosome of the first child
    if first == 1:
       child1.permut[0] = perm1[0]
       child2.permut[0] = perm2[0]
       index = 0
       while perm2[index] != child1.permut[0]:#while we didn't complete a cycle
           for i in range(size):
               if perm1[i] == perm2[index]:
                   child1.permut[i] = perm1[i]
                   child2.permut[i] = perm2[i]
                   index = i
                   break
       for i in range(size):
           if child1.permut[i] == -1:
               child1.permut[i] = perm2[i]
               child2.permut[i] = perm1[i]

    else:
        child1.permut[0] = perm2[0]
        child2.permut[0] = perm1[0]
        index = 0
        while perm1[index] != child1.permut[0]:
            for i in range(size):
                if perm2[i] == perm1[index]:
                    child1.permut[i] = perm2[i]
                    child2.permut[i] = perm1[i]
                    index = i
                    break
        for i in range(size):
            if child1.permut[i] == -1:
                child1.permut[i] = perm1[i]
                child2.permut[i] = perm2[i]

    return child1, child2

def simple_inverse_mutate(member):#inverse the string between specific range
    size = len(member.str)
    posi = randint(0, size-2)
    posj = randint(posi+1, size-1)
    if posi > posj:
        posi, posj = posj, posi
    while posi < posj:
        member.str[posi], member.str[posj] = member.str[posj], member.str[posi]
        posi += 1
        posj -= 1

def swap_mutate(member):#swaps two random indeces in the string
    size = len(member.str)
    posi = randint(0, size - 2)
    posj = randint(posi + 1, size - 1)
    str1 = ""
    str1 = member.str[0:posi] + member.str[posj] + member.str[posi + 1:posj]+ member.str[posi] + member.str[posj+1:]
    member.str = str1

def kendalldis(s1=[1, 2, 3, 4, 5, 6, 7],s2=[1, 3, 6, 2, 7, 4, 5]):
    corr, _ = kendalltau(s1, s2)
    print('Kendall Rank correlation: %.5f' % corr)

def kendallTau(A=[1, 2, 3, 4, 5, 6, 7], B=[1, 3, 6, 2, 7, 4, 5]):
    pairs = itertools.combinations(range(0, len(A)), 2)

    distance = 0

    for x, y in pairs:
        a = A[x] - A[y]
        b = B[x] - B[y]

        # if discordant (different signs)
        if (a * b < 0):
            distance += 1

    return distance











