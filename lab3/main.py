from CVRP import *
from City import *
from Vehicle import *
from GetInput import *
from SimulatedAnnealing import *

def CV():
    arr_city = []
    arr_veh = [0] * 5
    xcor = 5
    ycor = 2
    for i in range(4):
        city = City(xcor, ycor, 0)
        arr_city.append(city)
        xcor += 1
        ycor += 2

    #cv = CVRP(arr_city, arr_veh, arr_city[2])
    #mat= cv.Distance_mat(arr_city)
    #print(mat)
if __name__ == '__main__':
    problem = GetInput("\problem1.txt")
    Simulated_Annealing(problem, 100, 0.5, 2048, 1500, 25)