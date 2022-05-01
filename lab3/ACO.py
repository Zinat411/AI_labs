import math
import random
import numpy
import functools
import sys
import time





def getsol(indexes, distances, capacityLimit, demand, pheromones):
    solution = list()
    alpha = 2
    beta = 5
    while (len(indexes) != 0):
        path = list()
        node = numpy.random.choice(indexes)
        capacity = capacityLimit - demand[node]
        path.append(node)
        indexes.remove(node)
        #according to the algorithim - creating the probabilitie's map
        while (len(indexes) != 0):
            probabilities = list(map(lambda x: ((pheromones[(min(x, node), max(x, node))]) ** alpha) * (
                    (1 / distances[(min(x, node), max(x, node))]) ** beta), indexes))
            probabilities = probabilities / numpy.sum(probabilities)

            node = numpy.random.choice(indexes, p=probabilities)
            capacity = capacity - demand[node]

            if (capacity > 0):
                path.append(node)
                indexes.remove(node)
            else:
                break
        solution.append(path)
    return solution


def calcfitness(self, path):
    fitness = 0
    i = 0
    trucksnum = 1
    capacity = self.cvrp.capacity

    fitness += self.cvrp.Distance_mat()[path[i + 1] - 1][0]  # cost paid so far
    capacity -= self.cvrp.Cities[path[i] - 1].demand  # capacity left

    while i < (self.cvrp.dimension - 2):
        x = path[i]
        y = path[i + 1]
        # print(x," coor ",y)
        if self.cvrp.Cities[y - 1].demand <= capacity:
            cost = self.cvrp.Distance_mat()[x - 1][y - 1]
            capacity -= self.cvrp.Cities[y - 1].demand
            fitness += cost
        else:
            fitness += self.cvrp.Distance_mat()[x - 1][0]
            capacity = self.cvrp.capacity
            trucksnum += 1
            fitness += self.cvrp.Distance_mat()[y - 1][0]
            capacity -= self.cvrp.Cities[y - 1].demand
        i += 1

    fitness += self.cvrp.Distance_mat()[path[i] - 1][0]
    return fitness

def updatePheremons(pmatrix, Path, fitness):
    currentPheremons = [[float(0) for _ in range(len(pmatrix[0]))] for _ in range(len(pmatrix[0]))]
    for i in range(len(Path) - 1):
        currentPheremons[Path[i] - 1][Path[i + 1] - 1] = float(float(10) / float(fitness))
        currentPheremons[Path[i + 1] - 1][Path[i] - 1] = float(float(10) / float(fitness))

    for i in range(len(pmatrix[0])):
        for j in range(len(pmatrix[0])):
            num1 = float(pmatrix[i][j] * (1 - p))
            num2 = float(currentPheremons[i][j] * p)
            pmatrix[i][j] = float(num1 + num2)
            if pmatrix[i][j] < 0.0001:
                pmatrix[i][j] = 0.0001



def start(args,cvrp):


    best = []
    MAX_iterations = args.max_iter
    size = args.GA_POPSIZE

    for i in range(MAX_iterations):
        solutions = list()
        for j in range(size):
            solution = getsol(nodes.copy(), dist, capacityLimit, demands, pheromones)
            solutions.append((solution, calcfitness(solution, dist)))

        best = updatePheremons(pheromones, solutions, best)


    for path in best[0]:
        path.insert(0,"0")
        path.append("0")
        print(path)
