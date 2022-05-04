from City import *
from Vehicle import *
from math import sqrt
import random
class CVRP:
    def __init__(self, Dimension, Capacity, Cities ,Warehouse, matrix):
        self.Cities = Cities
        self.Dimension = Dimension
        self.Warehouse = Warehouse
        self.Capacity = Capacity
        self.best_tour = []
        self.best_cost = 0
        self.solution = []
        self.trucks = 0
        self.matrix = matrix

    def set_cities(self):
        self.Cities = self.Cities.pop(0)
    def print_result(self):
        print(self.best_cost)
        #print('the best tour', self.best_tour)
        all = self.Vehicles_tour(self.best_tour)
        for tour in all:
            print(*tour, sep=' ')
    def Vehicles_tour(self, tour): #this function returns the path for every vehicle given the whole path permutation
        first = 0 #index for the first of the vehicle's path
        last = 0  #index for the last of the vehicle's path
        veh_capacity = self.Capacity
        veh_arr = []
        veh_capacity -= self.Cities[tour[last] - 1].demand
        tour_length = len(tour)
        veh_num = 1
        while last < tour_length - 1:
            curr = tour[last + 1]
            if self.Cities[curr - 1].demand <= veh_capacity:
                veh_capacity -= self.Cities[curr - 1].demand #this vehicle can supply the demand of this city
            else:
                veh_arr.append(tour[first: last+1])
                first = last + 1
                veh_capacity = self.Capacity - self.Cities[curr - 1].demand
            last += 1
        veh_arr.append(tour[first:tour_length])
        #to saperate every vehicle's tour from one anthor we added -1 between them in the original array
        for veh_tour in veh_arr:
            veh_tour.insert(0, 0)
            veh_tour.append(0)

        return veh_arr

    def tour_cost_veh(self, tour):# this function calculates the cost of the vehicle's tour
        matrix = self.matrix
        count = 0
        count += matrix[tour[0]][0]
        last = len(tour)
        veh_capacity = self.Capacity - self.Cities[tour[0] - 1].demand
        for i in range(last - 2):
            curr = tour[i]
            target = tour[i+1]
            if self.Cities[target-1].demand <= veh_capacity:
                veh_capacity -= self.Cities[target-1].demand
                count += matrix[curr][target]
            else:
                count += matrix[curr][0] + matrix[target][0]
                veh_capacity = self.Capacity - self.Cities[target - 1].demand

        count += matrix[tour[last - 1]][0]
        return count
#**********************ACO functions**************************
    def cal(i, j, pmat, dmat):
        return float(pow(float(pmat[i][j]), 2) * pow(float(1 / float(dmat[i + 1][j + 1])), 2))
    def acophmatrix(acophmatrix, path, cost):
        current = [[float(0) for _ in range(len(acophmatrix[0]))] for _ in range(len(acophmatrix[0]))]
        for i in range(len(path) - 1):
            current[path[i] - 1][path[i + 1] - 1] = float(float(2) / float(cost))
            current[path[i + 1] - 1][path[i] - 1] = float(float(2) / float(cost))

        for i in range(len(acophmatrix[0])):
            for j in range(len(acophmatrix[0])):
                num1 = float(acophmatrix[i][j] * (1 - 2))
                num2 = float(current[i][j] * 2)
                acophmatrix[i][j] = float(num1 + num2)
                if acophmatrix[i][j] < 0.0001:
                    acophmatrix[i][j] = 0.0001

    def getp(currentCity, pmat):
        v = []
        s = sum(pmat[currentCity - 1][:])
        for i in range(len(pmat[0])):
            v.append(float(float(pmat[currentCity - 1][i]) / float(s)))
        return v


    def updatemat(current, pmat):
        for i in range(len(pmat[0])):
            pmat[current - 1][i] = float(0)
            pmat[i][current - 1] = float(0)







