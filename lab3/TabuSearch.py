from datetime import time

from lab3 import Arguments
from lab3.CVRP import CVRP
import random
from Heuristic import *
import time
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
        best=get_best_neighbor(self.cvrp, len(self.cvrp.Cities))
        random.shuffle(best)
        fitness = self.cvrp.tour_cost_veh(best) #best fitness->fitness
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
            min= self.cvrp.tour_cost_veh(temp)

            for n in neighborhood:
                cost= self.cvrp.tour_cost_veh(n)
                if cost < min and not recent.get(str(n), False):
                    min = cost
                    temp = n
            if min < fitness:  # update best (take a step towards the better neighbor)
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


