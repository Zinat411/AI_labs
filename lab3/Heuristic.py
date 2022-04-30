from random import randint
from CVRP import *

def get_best_neighbor(problem, size):
    arr = []
    is_available = [0] * size
    city = randint(1, size)
    arr.append(city)
    is_available[city] = 1
    index = size - 1
    while index > 0:
        matrix = problem.Distance_mat()
        sub_arr = matrix[city]
        min_dis = float('inf')
        for i in range(1, len(sub_arr)):
            if sub_arr[i] < min_dis and is_available[i] == 0:
                min_dis = sub_arr[i]
                min_city = i
        arr.append(min_city)
        is_available[min_city] = 1
        index -= 1
        city = min_city
    return arr

def get_all_neighborhood(best, size):
     neighborhood = []
     for i in range(size):
         neighborhood.append(swap_mutation(best))
     return neighborhood


def swap_mutation(tour):
    # Swap two positions in the tour.
    size = len(tour)
    pos1 = random.randint(0, size - 2)
    pos2 = random.randint(pos1 + 1, size - 1)
    newTour = tour[0:pos1] + [tour[pos2]] + tour[pos1 + 1:pos2] + [tour[pos1]] + tour[pos2 + 1:]
    return newTour