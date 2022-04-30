from City import *
from Vehicle import *
from math import sqrt
import random
class CVRP:
    def __init__(self, Dimension, Capacity, Cities ,Warehouse):
        self.Cities = Cities
        self.Dimension = Dimension
        self.Warehouse = Warehouse
        self.Capacity = Capacity

    def Distance_mat(self):
        Cities = self.Cities
        numCities = len(Cities)
        rows, cols = numCities, numCities
        arr = [[0]*rows]*cols
        for i in range(rows):
            for j in range(cols):
                dx = (Cities[i].Xcor - Cities[j].Xcor) * (Cities[i].Xcor - Cities[j].Xcor)
                dy = (Cities[i].Ycor - Cities[j].Ycor) * (Cities[i].Ycor - Cities[j].Ycor)
                distance = sqrt(dx + dy)
                arr[i][j] = distance
                arr[j][i] = distance
        return arr

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
                veh_num += 1
                veh_capacity = self.Capacity - self.Cities[curr - 1].demand
            last += 1
        veh_arr.append(tour[first:tour_length])
        #to saperate every vehicle's tour from one anthor we added -1 between them in the original array
        for veh_tour in veh_arr:
            veh_tour.append(-1)
            veh_tour.insert(0, -1)

        return veh_arr

    def tour_cost_veh(self, tour, cities):# this function calculates the cost of the vehicle's tour
        matrix = self.Distance_mat()
        count = matrix[tour[0]][0]
        last = len(tour)
        veh_capacity = self.Capacity - self.Cities[tour[0] - 1].demand
        for i in range(last - 1):
            curr = tour[i]
            target = tour[i+1]
            if self.Cities[target-1].demand <= veh_capacity:
                count += matrix[curr][target]
                veh_capacity -= self.Cities[target-1].demand
            else:
                count += matrix[curr][0]
                veh_capacity = self.Capacity - self.Cities[target - 1].demand
                count += matrix[target][0]# new tour for new vehicle starting at target

        count += matrix[tour[last - 1]][0]
        return count








