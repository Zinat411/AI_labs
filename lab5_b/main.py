
import time
from timeit import default_timer as timer
from matplotlib import pyplot as plt

from Agent import Agent
from Arguments import Var
from Genitic5 import Genetic5
from NW import NW
from readData import readData
W = 0.5
c1 = 0.8
c2 = 0.9
num_iter = 50
n_particles = 30
target = 'Hello World!'
target_error = 0.000001
ARGS = Var(50, 1000, 0.1, 0.5,None,None,None,None )

def run(ga, args1, esize, start_elapsed):
    lst = []


    ga.calc_fitness(ga.population)
    ga.sort_by_fitness(ga.population)
    bestfitness=ga.population[0].fitness
    ga.best = ga.population[0]
    for i in range(args1.maxiter):
        iteration_time = time.time()
        ga.calc_fitness(ga.population)
        ga.sort_by_fitness(ga.population)
        if ga.population[0].fitness < bestfitness:
            ga.best=ga.population[0]
            ga.best=Agent(ga.population[0].arr,ga.population[0].fitness,ga.population[0].network)
            ga.best.age=ga.population[0].age
            ga.best.reg=ga.population[0].reg
            bestfitness=ga.population[0].fitness
        # ga.print_best(ga.population)
        print("fitness: ", bestfitness)
        print("best agent: ",ga.best.arr)

        lst.append(bestfitness)
        if ga.population[0].fitness == 0:
            print()
            print("Best string: ", ga.population[0].arr)
            print(f'found in {i} iterations out of {args1.maxiter}')
            elapsed_time = timer() - start_elapsed
            print("Elapsed time: ", elapsed_time)
            break
        ga.mate()
        clock_ticks = time.time() - iteration_time
        print("Clock ticks time: ", clock_ticks)
    ga.match()
    ga.tournament()
    fig, ax = plt.subplots()
    gennumarr = []
    for i in range(len(lst)):
        gennumarr.append(i)
    ax.plot(gennumarr, lst)
    plt.xlabel('iteration num')
    plt.ylabel('fitness')
    plt.show()


def GArun(cross_type):
    start_qt = time.time()  # the start time of clock ticks
    start_elapsed = timer()  # the start time of elapsed
    args1 = get_input()
    ga = Genetic5(args1)
    esize = int(args1.GA_POPSIZE * args1.GA_ELITRATE)
    ga.init_population()
    run(ga, args1, esize, start_elapsed)

def get_input():
    popsize = 8
    maxIter = 100
    rd = readData()

    train_x, train_y, test_x, test_y = rd.readData()
    nw = NW(train_x, train_y, test_x, test_y)
    nw.mlpFunc()

    args = Var(maxIter, popsize, 0.1, 0.1,train_x, train_y, test_x, test_y)
    ARGS = args
    return args


if __name__ == '__main__':
   GArun(ARGS)

