from Heuristic import *
from CVRP import *
import time
from numpy import exp
from numpy.random import rand
import matplotlib.pyplot as plt

def Simulated_Annealing(problem, temp, alpha, neighbor_size, maxIter, stop):
    start = time.time()
    size = len(problem.Cities)
    best_neighbor = get_best_neighbor(problem, size)
    for i in range(len(best_neighbor) - 1 ):
        if best_neighbor[i] == best_neighbor[i+1]:
             best_neighbor.pop(i+1)
    best_tour = problem.tour_cost_veh(best_neighbor, problem.Cities)
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
            randTour = problem.tour_cost_veh(randNeigh, problem.Cities)
            d = randTour - best_tour
            result = float(exp(float(-1 * d) / temp1))
            if randTour < curr_best_tour:
                curr_best_neigh = randNeigh
                curr_best_tour = randTour
            elif result > rand():
                curr_best_neigh = randNeigh
                curr_best_tour = randTour
        if curr_best_tour < best_tour:
            best_neighbor = curr_best_neigh
            best_tour = curr_best_tour
            optimum = 0
        elif curr_best_tour == best_tour:# when local optimum is found
            optimum += 1
        if best_tour < final_best_tour:
            final_best_neigh = best_neighbor
            final_best_tour = best_tour
        if optimum == stop:# restart
            if best_tour < final_best_tour:
                final_best_neigh = best_neighbor
                final_best_tour = best_tour
                best_neighbor = get_best_neighbor(problem, size)
                best_tour = problem.tour_cost_veh(best_neighbor, problem.Cities)
                curr_best_neigh = best_neighbor
                curr_best_tour = best_tour
                optimum = 0
                temp1 = float(temp1)
            print('result: ', best_neighbor)
            print('total: ',best_tour)
            print('clock ticks:', time.time() - iterTime)
            temp1 *= alpha
            #print('temp', temp1)
    print('Time elapsed: ', time.time() - start)
    problem.best_tour = final_best_neigh
    problem.best_cost = final_best_tour
    x = [i for i in range(maxIter)]
    plt.scatter(x, y)
    plt.title('The relation between iteration and the cost')
    plt.xlabel('iteration num')
    plt.ylabel('cost')
    plt.show()

def restart(optimum, stop, best_tour, final_best_tour, best_neighbor, problem, size, temp1):
    best_neighbor = get_best_neighbor(problem, size)
    best_tour = problem.tour_cost_veh(best_neighbor, problem.Cities)
    curr_best_neigh = best_neighbor
    curr_best_tour = best_tour
    optimum = 0
    temp1 = float(temp1)
    return best_neighbor, best_tour, temp1,  curr_best_neigh,final_best_tour

