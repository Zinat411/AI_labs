from Heuristic import *
from CVRP import *
import time
from numpy import exp
from numpy.random import rand, random
import matplotlib.pyplot as plt
import copy
from numpy.random import uniform
import math

def Simulated_Annealing(problem, temp, alpha, neighbor_size, maxIter, stop):
    start = time.time()
    size = len(problem.Cities)
    # best_neighbor = get_best_neighbor(problem, size)
    best_neighbor= uniform(-32.768, 32.768, 10)
    #print('in sim ann with best_neighbor', best_neighbor)
    #for i in range(len(best_neighbor) - 1 ):
        #if best_neighbor[i] == best_neighbor[i+1]:
             #best_neighbor.pop(i+1)
    calc = 0
    calc2 = 0
    for i in range(10):
        calc += ((best_neighbor[i]) ** 2)
        calc2 += math.cos(2 * math.pi * best_neighbor[i])
    best_tour = -20.0 * math.exp(-0.2 * math.sqrt(0.1 * calc)) - math.exp(0.1 * calc2) + 1 + 20
    # best_tour = problem.tour_cost_veh(best_neighbor)

    #print('best tour is:', best_tour)
    curr_best_neigh = best_neighbor
    curr_best_tour = best_tour
    final_best_neigh = best_neighbor
    final_best_tour = best_tour
    k = 30
    optimum = 0
    temp1 = float(temp)
    y = []
    for i in range(maxIter):
        iterTime = time.time()
        neighborhood = get_all_neighborhood(best_neighbor, neighbor_size)
        y.append(best_tour)
        for j in range(k):
            index = randint(0, len(neighborhood) - 1)
            randNeigh = neighborhood[index]
            # randTour = problem.tour_cost_veh(randNeigh)
            calc = 0
            calc2 = 0
            for i in range(10):
                calc += ((randNeigh[i]) ** 2)
                calc2 += math.cos(2 * math.pi * randNeigh[i])
            randTour = -20.0 * math.exp(-0.2 * math.sqrt(0.1 * calc)) - math.exp(0.1 * calc2) + 1 + 20

            d = randTour - best_tour
            if d!=0:
              result = float(exp(float(-1 * d) / temp1))
            else:
                result=0
            if randTour < curr_best_tour:
                curr_best_neigh = copy.deepcopy(randNeigh)
                curr_best_tour = randTour
            elif result > random():
                curr_best_neigh = copy.deepcopy(randNeigh)
                curr_best_tour = randTour
        if curr_best_tour < best_tour:
            best_neighbor = curr_best_neigh
            best_tour = curr_best_tour
            optimum = 0
        if curr_best_tour == best_tour:# when local optimum is found
            optimum += 1
        if best_tour < final_best_tour:
            final_best_neigh = best_neighbor
            final_best_tour = best_tour
        if optimum == stop:# restart
            if best_tour < final_best_tour:
                final_best_neigh = best_neighbor
                final_best_tour = best_tour
            # best_neighbor = get_best_neighbor(problem, size)
            best_neighbor=uniform(-32.768, 32.768, 10)
            # best_tour = problem.tour_cost_veh(best_neighbor)
            calc = 0
            calc2 = 0
            for i in range(10):
                calc += ((best_neighbor[i]) ** 2)
                calc2 += math.cos(2 * math.pi * best_neighbor[i])
            best_tour = -20.0 * math.exp(-0.2 * math.sqrt(0.1 * calc)) - math.exp(0.1 * calc2) + 1 + 20

            curr_best_neigh = best_neighbor
            curr_best_tour = best_tour
            optimum = 0
            temp1 = float(temp)
        print('result: ', best_neighbor)
        print('total: ',best_tour)
        print('clock ticks:', time.time() - iterTime)
        temp1 *= alpha
    print('Time elapsed: ', time.time() - start)
    problem.best_tour = final_best_neigh
    problem.best_cost = final_best_tour
    x = [i for i in range(maxIter)]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    #plt.scatter(x, y)
    #plt.title('The relation between iteration and the cost')
    plt.xlabel('iteration num')
    plt.ylabel('fitness')
    plt.show()

def restart(optimum, stop, best_tour, final_best_tour, best_neighbor, problem, size, temp1):
    best_neighbor = get_best_neighbor(problem, size)
    best_tour = problem.tour_cost_veh(best_neighbor, problem.Cities)
    curr_best_neigh = best_neighbor
    curr_best_tour = best_tour
    optimum = 0
    temp1 = float(temp1)
    return best_neighbor, best_tour, temp1,  curr_best_neigh,final_best_tour

