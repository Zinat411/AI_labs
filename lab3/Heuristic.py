from random import randint
from CVRP import *

def get_best_neighbor(problem, size):
    arr = []
    city = randint(1, size)
    arr.append(city)
    #print('city', city)
    is_available = {city: True}
    index = size - 1
    while index > 0:
        matrix = problem.matrix
        sub_arr = matrix[city]
        #print('len sub array', len(sub_arr))
        #print('sub arr', sub_arr)
        min_dis = float('inf')
        min_city = 1
        for i in range(1, len(sub_arr)):
            #print('is available:', is_available.get(i))
            if sub_arr[i] < min_dis and not is_available.get(i, False):
                min_dis = sub_arr[i]
                #print('**************', 'i', i+1 , 'sub_arr[i]', sub_arr[i])
                min_city = i
                #print('min city', min_city, 'value', sub_arr[i])
        arr.append(min_city)
        is_available[min_city] = True
        #print('arr', arr)
        #print('is available ', is_available)
        index -= 1
        city = min_city

    return arr

def get_all_neighborhood(best, size):
     neighborhood = []
     for i in range(size):
         neighborhood.append(simple_inverse_mutate(best))
     return neighborhood

def simple_inverse_mutate(member):#inverse the string between specific range
    tmp = member[:]
    size = len(member)
    posi = randint(0, size-1)
    posj = randint(0, size-1)
    if posi > posj:
        posi, posj = posj, posi
    while posi < posj:
        tmp[posi], tmp[posj] = tmp[posj], tmp[posi]
        posi += 1
        posj -= 1
    return tmp
def swap_mutation(tour):
    # Swap two positions in the tour.
    size = len(tour)
    pos1 = random.randint(0, size - 2)
    pos2 = random.randint(pos1 + 1, size - 1)
    newTour = tour[0:pos1] + [tour[pos2]] + tour[pos1 + 1:pos2] + [tour[pos1]] + tour[pos2 + 1:]
    return newTour