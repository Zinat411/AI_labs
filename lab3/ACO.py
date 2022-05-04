from math import pow
from random import randint
from numpy.random import choice
import time

from lab3.CVRP import CVRP


def ACO(cv:CVRP, args):
    startTime = time.time()
    # start time
    pmatrix = [[float(1000) for _ in range(len(cv.Cities))] for _ in range(len(cv.Cities))]
    # initialize the p matrix
    bestPath = []
    fitlst=[]
    bestFitness = float('inf') #start with infinite fitness
    currentPath = []
    currentFitness = float('inf')
    globalBest = []
    globalFitness = float('inf')
    counter = 0
    for k in range(args.maxiter):
        iterTime = time.time()
        temp = getPath(cv, pmatrix)
        tempFitness = cv.tour_cost_veh(temp)
        if tempFitness < currentFitness:
            currentFitness = tempFitness
            currentPath = temp
        if currentFitness < bestFitness:  # update best (take a step towards the better neighbor)
            bestFitness = currentFitness
            bestPath = currentPath
            counter = 0
        if currentFitness == bestFitness:   # to detect local optimum
            counter += 1
        if bestFitness < globalFitness:# update the best solution found untill now
            globalBest = bestPath
            globalFitness = bestFitness
        CVRP.acophmatrix(pmatrix, temp, tempFitness)
        print('clock ticks: ', time.time() - iterTime)
        print('best solution is: ', bestPath)
        print('cost is: ', bestFitness)
        fitlst.append(bestFitness)
        print()
        if counter == 25:  #local optima
            pmatrix = [[float(1000) for _ in range(len(cv.Cities))] for _ in range(len(cv.Cities))]
            counter = 0
            if bestFitness < globalFitness:
                globalBest = bestPath
                globalFitness = bestFitness
            bestPath = []
            bestFitness = float('inf')
            currentPath = []
            currentFitness = float('inf')
    print('Time elapsed: ', time.time() - startTime)
    cv.best_tour = globalBest   # save the solution and its fitness
    cv.best_cost = globalFitness
    return fitlst


def getPath(cvpr, pmatrix):
    citylst = [i + 1 for i in range(len(cvpr.Cities))]
    pmat = []
    for i in range(len(cvpr.Cities)):
        problst = []
        for j in range(len(cvpr.Cities)):
            x = 0
            if i != j:
                x = CVRP.cal(i, j, pmatrix, cvpr.matrix)
            problst.append(x)
        pmat.append(problst)
    currentCity = randint(1, len(citylst))
    citylst[currentCity - 1] = -1
    path = [currentCity]
    while len(citylst) != len(path):
        pvec = CVRP.getp(currentCity, pmat)
        CVRP.updatemat(currentCity, pmat)
        currentCity = choice(citylst, p=pvec)
        citylst[currentCity - 1] = -1

        path.append(currentCity)


    return path


