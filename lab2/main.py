import time
from Genetic5 import *
from Arguments import *
from Struct import *
from Functions import *
from Nqueens import NQueens
from MinimalConflicts import MinimalConflicts
from timeit import default_timer as timer
from Baldwin import  *
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt


W = 0.5
c1 = 0.8
c2 = 0.9
num_iter = 50
n_particles = 30
target = 'Hello World!'
target_error = 0.000001
ARGS=Var(0, 0, 0, 0, "targetString", "cross_type")

def run(ga, population, buffer, args1, esize, start_elapsed):
    if(args1.problem==4):
        incorrectarr=[]
        correctarr=[]
        fixedarr=[]
        gennumarr = []
        fig, ax = plt.subplots()
        fig,ax2 = plt.subplots()
        fig, ax3 = plt.subplots()



    for i in range(args1.GA_MAXITER):
        iteration_time = time.time()
        if (args1.problem != 4):# if it's not the balwin experiment
            # if(i%args1.frequency==0):
              # call learning algorithm
              # ga.calc_fitness()

            ga.calc_fitness(population)
        else:
            incorrect,correct,fixed=ga.calc_fitness(population)
            incorrectarr.append(incorrect)
            correctarr.append(correct)
            fixedarr.append(fixed)
        ga.sort_by_fitness(population)
        ga.print_best(population)
       # if args1.problem==1:
        # ga.selection_pressure(population)
        #avgfitness = ga.calc_avg_fitness(population)
        #print("The average of the fitness is:", avgfitness)
        #standard_dv = ga.calc_SD(population, avgfitness)
        #print("The standard deviation is: ", standard_dv)

        if population[0].getFitness() == 0 and args1.problem!=4:
            print()
            print("Best string: " + population[0].str)
            print(f'found in {i} iterations out of {args1.GA_MAXITER}')
            elapsed_time = timer() - start_elapsed
            if args1.problem==1:
               norm_fitness = normalize(population, args1)

               histogram(norm_fitness, population, args1)
            print("Elapsed time: ", elapsed_time)

            break

        ga.mate(population, buffer)
        clock_ticks = time.time() - iteration_time
        print("Clock ticks time: ", clock_ticks)
        population, buffer = buffer, population
    if(args1.problem==4):
        for i in range(len(correctarr)):
            gennumarr.append(i)
        ax.plot(incorrectarr, gennumarr)
        ax.set_title('incorrect')
        ax.set_xlabel("Incorrect percentage")
        ax.set_ylabel("generation")

        ax2.plot(correctarr, gennumarr)
        ax2.set_title('correct')
        ax2.set_xlabel("correct percentage")
        ax2.set_ylabel("generation")

        ax3.plot(fixedarr, gennumarr)
        ax3.set_title('fixed')
        ax3.set_xlabel("fixed bits percentage")
        ax3.set_ylabel("generation")

        plt.show()

def single():
    GArun("Single")

def two():
    GArun("Two")

def uniform():
    GArun("Uniform")

def GArun(cross_type):
    start_qt = time.time()  # the start time of clock ticks
    start_elapsed = timer()  # the start time of elapsed
    args1 = get_input()


    if (args1.problem==1or args1.problem==4):

        if(args1.problem==4):
            ga=Baldwin(args1)
        else:
            ga = Genetic5(args1)
        if (cross_type == "Single"):
            args1.CROSS_TYPE = "Single"
        elif (cross_type == "Two"):
            args1.CROSS_TYPE = "Two"
        elif (cross_type == "Uniform"):
            args1.CROSS_TYPE = "Uniform"
    elif (args1.problem==2):
        ga = NQueens(args1)
    elif (args1.problem==3):
        m = MinimalConflicts(args1)
        m.init()

    if(args1.problem!=3):
        esize = int(args1.GA_POPSIZE * args1.GA_ELITRATE)
        pop_alpha = [None] * args1.GA_POPSIZE
        pop_beta = [None] * args1.GA_POPSIZE
        ga.init_population(pop_alpha, pop_beta)
        population = pop_alpha
        buffer = pop_beta

        run(ga, population, buffer, args1, esize, start_elapsed)




def get_input():
    numQueens=8
    targetString=""
    cross_type="Uniform"
    problem = int(input("please enter problem number: \n"
                        "1 for String matching\n"
                        "2 for Nqueens\n"
                        "3 for Minimal Conflicts\n"
                        "4 for baldwin\n"
                        ))
    popsize = 2048
    maxIter = 16384
    frequency=1000
    intensity=5
    if(problem==4):
        maxIter=20
        popsize=1000
    eliteRate = 0.1
    mutationRate = 0.5
    if (problem==1or problem==4):
       targetString = input("please enter text: ")
       crossT = input("please enter crossing type: ")

       cross_type = crossT

    else:
        numQueens=int(input("please enter the number of queens: "))
    args = Var(popsize, maxIter, eliteRate, mutationRate, targetString, cross_type,problem,frequency,intensity,numQueens)
    ARGS=args
    return args

if __name__ == '__main__':
        GArun(ARGS)