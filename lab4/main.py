import time
from timeit import default_timer as timer
from tkinter import *
import numpy as np
from Arguments import *
from Genetic5 import *
from Struct import *


W = 0.5
c1 = 0.8
c2 = 0.9
num_iter = 50
n_particles = 30
target = 'Hello World!'
target_error = 0.000001
ARGS=Var(50,1000, 0.1, 0.5)

def run(ga,args1, esize, start_elapsed):

    for i in range(args1.maxiter):
        iteration_time = time.time()


        ga.calc_fitness(ga.population)

        ga.sort_by_fitness(ga.population)
        ga.print_best(ga.population)

        if ga.population[0].fitness == 0 :
            print()
            print("Best string: " , ga.population[0].arr)
            ga.print_sorted(ga.population[0].arr)
            print(f'found in {i} iterations out of {args1.maxiter}')
            elapsed_time = timer() - start_elapsed
            print("Elapsed time: ", elapsed_time)

            break

        ga.mate(ga.population, ga.buffer)
        clock_ticks = time.time() - iteration_time
        print("Clock ticks time: ", clock_ticks)
        ga.population,ga.buffer = ga.buffer, ga.population



def GArun(cross_type):
    start_qt = time.time()  # the start time of clock ticks
    start_elapsed = timer()  # the start time of elapsed
    args1 = get_input()
    ga = Genetic5(args1)
    esize = int(args1.GA_POPSIZE * args1.GA_ELITRATE)
    # pop_alpha = [None] * args1.GA_POPSIZE
    # pop_beta = [None] * args1.GA_POPSIZE
    # ga.population = pop_alpha
    # buffer = pop_beta
    ga.init_population()
    print(ga.population[1])


    run(ga,args1, esize, start_elapsed)




def get_input():
    popsize = 2048
    maxIter = 16384

    args = Var(maxIter,popsize,0.1,0.5)
    ARGS=args
    return args

if __name__ == '__main__':
    print("main")
    GArun(ARGS)