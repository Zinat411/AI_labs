from datetime import time

from lab3 import Arguments
from lab3.CVRP import CVRP
import random

class TabuSearch:
    def __init__(self,cvrp: CVRP,args:Arguments):

        self.args=args
        self.cvrp=cvrp

    def SwapMove(self,solution, city1, city2):
        solution = solution.copy()
        city1pos = solution.index(city1)
        city2pos = solution.index(city2)
        solution[city1pos], solution[city2pos] = solution[city2pos], solution[city1pos]
        return solution

    def findneighbor(self,path):
        neighbors=[]
        for i in range(self.cvrp.Dimension):
             neighbors.append(self.SwapMove(path, random.randint(1, self.cvrp.Dimension),random.randint(1, self.cvrp.Dimension)))
        return neighbors

    def calcfitness(self,path):
        fitness = 0
        i=0
        trucksnum=1
        capacity = self.cvrp.Capacity

        fitness += self.cvrp.Distance_mat()[path[i+1]-1][0] #cost paid so far
        capacity -= self.cvrp.Cities[path[i] - 1].demand #capacity left


        while i < (self.cvrp.Dimension-2):
            x = path[i]
            y = path[i + 1]
            # print(x," coor ",y)
            if self.cvrp.Cities[y - 1].demand <= capacity:
                cost = self.cvrp.Distance_mat()[x-1][y-1]
                capacity -= self.cvrp.Cities[y - 1].demand
                fitness += cost
            else:
                fitness += self.cvrp.Distance_mat()[x-1][0]
                capacity = self.cvrp.Capacity
                trucksnum += 1
                fitness += self.cvrp.Distance_mat()[y-1][0]
                capacity -= self.cvrp.Cities[y - 1].demand
            i += 1

        fitness += self.cvrp.Distance_mat()[path[i]-1][0]
        return fitness

    def start(self):
        lst=[]
        best=list(range(1,self.cvrp.Dimension+1))
        random.shuffle(best)
        fitness = self.calcfitness(best) #best fitness->fitness
        lst.append(fitness)
        temp = best #bestcandidate->temp
        recent = {str(best): True}#check at the end

        recentcities = [best]
        for j in range(self.args.maxiter):

            neighborhood = self.findneighbor(temp)  # get neighborhood of current solution
            temp = neighborhood[0]
            min= self.calcfitness(temp)

            for n in neighborhood:
                cost= self.calcfitness(n)
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
        return lst


