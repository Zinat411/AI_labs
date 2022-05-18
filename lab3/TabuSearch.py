from datetime import time

from lab3 import Arguments
from lab3.CVRP import CVRP
import random
from Heuristic import *
import time
from numpy.random import uniform
import math
class TabuSearch:
    def __init__(self,cvrp,args:Arguments):

        self.args=args
        self.cvrp=cvrp

    def SwapMove(self,solution, city1, city2):
        solution = solution.copy()
        city1pos = solution.index(city1)
        city2pos = solution.index(city2)
        solution[city1pos], solution[city2pos] = solution[city2pos], solution[city1pos]
        return solution

    def start(self):
        lst=[]
        # best=get_best_neighbor(self.cvrp, len(self.cvrp.Cities))
        best=uniform(-32.768,32.768,10)
        # random.shuffle(best)
        calc=0
        calc2=0
        for i in range(10):
            calc += ((best[i]) ** 2)
            calc2 += math.cos(2 * math.pi * best[i])
        fitness = -20.0 * math.exp(-0.2 * math.sqrt(0.1 * calc)) - math.exp(0.1 * calc2) + 1 + 20
        # fitness = self.cvrp.tour_cost_veh(best) #best fitness->fitness
        lst.append(fitness)
        temp = best #bestcandidate->temp
        recent = {str(best): True}#check at the end
        y = []

        recentcities = [best]
        for j in range(self.args.maxiter):
            iterTime = time.time()
            neighborhood = get_all_neighborhood(temp, self.cvrp.Dimension)
            y.append(fitness)
            #neighborhood = self.findneighbor(temp)  # get neighborhood of current solution
            temp = neighborhood[0]
            # min= self.cvrp.tour_cost_veh(temp)
            calc = 0
            calc2 = 0
            for i in range(10):
                calc += ((temp[i]) ** 2)
                calc2 += math.cos(2 * math.pi * temp[i])
            min = -20.0 * math.exp(-0.2 * math.sqrt(0.1 * calc)) - math.exp(0.1 * calc2) + 1 + 20

            for n in neighborhood:
                # cost= self.cvrp.tour_cost_veh(n)
                # print("n is:",n)
                calc = 0
                calc2 = 0
                for i in range(10):
                    calc += ((n[i]) ** 2)
                    calc2 += math.cos(2 * math.pi * n[i])
                cost = -20.0 * math.exp(-0.2 * math.sqrt(0.1 * calc)) - math.exp(0.1 * calc2) + 1 + 20
                if cost < min and not recent.get(str(n), False):
                    print("test")
                    min = cost
                    temp = n
            if min < fitness:  # update best (take a step towards the better neighbor)
                print("best2 is:",best)
                fitness = min
                best = temp
            recentcities.append(temp)
            recent[str(temp)] = True
            if len(recentcities) > self.args.lastN:
                recent[str(recentcities[0])] = False
                recentcities.pop(0)

            print("best solution is: ", best)
            print("cost is: ", fitness)
            lst.append(fitness)
        self.cvrp.best_tour = best
        self.cvrp.best_cost = fitness
        return lst


