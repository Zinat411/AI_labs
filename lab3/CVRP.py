from City import *
from Vehicle import *
from math import sqrt
class CVRP:
    def __init__(self, Cities, Vehicles, Warehouse):
        self.Cities = Cities
        self.Vehicles = Vehicles
        self.Warehouse = Warehouse

    def Distance_mat(self, Cities):
        numCities = len(Cities)
        rows, cols = (numCities, numCities)
        arr = [[0]*rows]*cols
        for i in range(rows):
            for j in range(cols):
                dx = (Cities[i].Xcor - Cities[j].Xcor) * (Cities[i].Xcor - Cities[j].Xcor)
                dy = (Cities[i].Ycor - Cities[j].Ycor) * (Cities[i].Ycor - Cities[j].Ycor)
                distance = sqrt(dx + dy)
                arr[i][j] = distance
        return arr

