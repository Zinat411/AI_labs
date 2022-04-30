from Heuristic import *
from CVRP import *
import time
from numpy import exp
from numpy.random import rand

def Simulated_Annealing(problem, temp, alpha, neighbor_size, maxIter, stop):
    start = time.time()
    size = len(problem.Cities)
    best_neighbor = get_best_neighbor(problem, size)
    best_tour = problem.tour_cost_veh(best_neighbor, problem.Cities)
    curr_best_neigh = best_neighbor
    curr_best_tour = best_tour
    final_best_neigh = best_neighbor
    final_best_tour = best_tour
    k = 30
    optimum = 0
    for i in range(maxIter):
        iterTime = time.time()
        neighborhood = get_all_neighborhood(best_neighbor, neighbor_size)
        for j in range(k):
            index = randint(0, len(neighborhood) - 1)
            randNeigh = neighborhood[index]
            randTour = problem.tour_cost_veh(randNeigh, problem.Cities)
            d = randTour - best_tour
            if randTour < curr_best_tour:
                curr_best_neigh = randNeigh
                curr_best_tour = randTour
            elif float(exp(float(-1 * d) / temp)) > rand():
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
                best_neighbor, best_tour, temp, final_best_neigh, final_best_tour = restart(optimum, stop, best_tour, final_best_tour, best_neighbor, problem, size, temp)
        print('result: ', best_neighbor)
        print('fitness: ',best_tour)
        print('clock ticks:', time.time() - iterTime)
        temp = temp * alpha
    print('Time elapsed: ', time.time() - start)



def restart(optimum, stop, best_tour, final_best_tour, best_neighbor, problem, size, temp):
    best_neighbor = get_best_neighbor(problem, size)
    best_tour = problem.tour_cost_veh(best_neighbor, problem.Cities)
    curr_best_neigh = best_neighbor
    curr_best_tour = best_tour
    optimum = 0
    temp1 = float(temp)
    return best_neighbor, best_tour, temp1, final_best_tour

