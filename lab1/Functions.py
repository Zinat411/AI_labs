from Genetic5 import *
from Arguments import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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




