from CVRP import *
from City import *
from Vehicle import *
from GetInput import *
from SimulatedAnnealing import *
import time
from matplotlib import pyplot as plt
import Arguments
from lab3.Genetic5 import Genetic5
from lab3.TabuSearch import TabuSearch
from SimulatedAnnealing import *
from timeit import default_timer as timer

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
def gastart(args,cvrp):
    population = []
    buffer = []
    fitlst=[]
    ga = Genetic5(args, cvrp)
    ga.init_population(population, buffer)
    for i in range(args.maxiter):
        for pop in population:
            pop.fitness = ga.calcfitness(pop.str)
        ga.sort_by_fitness(population)
        ga.print_best(population)
        fitlst.append(population[0].fitness)
        if population[0].getFitness() == 0:
            print()
            print("Best string: " + str(population[0].str))
            print(f'found in {i} iterations out of {args.maxiter}')
            break
        ga.mate(population, buffer)
        population, buffer = buffer, population
    return fitlst

if __name__ == '__main__':
    fig, ax = plt.subplots()
    args = Arguments.Var(50, 1000, 20, 0.1, 0.5)  # (self, maxiter,lastN,popsize,eliteRate, mutationRate,):
    # ts=TabuSearch(cvrp,args)
    # ts.start()
    problem = int(input("please enter problem number: 1-5 \n"
                        ))
    if (problem == 1):
        cvrp = GetInput("\problem1.txt")
        #cvrp.print_result()
    if (problem == 2):
        cvrp = GetInput("\E-n33-k4.txt").cvrp
    if (problem == 3):
        cvrp = GetInput("\E-n51-k5.txt").cvrp
    if (problem == 4):
        cvrp = GetInput("\E-n76-k8.txt").cvrp
    if (problem == 5):
        cvrp = GetInput("\E-n76-k10.txt").cvrp
    algo = int(input("please enter algo number:\n"
                     "1 for tabu searchn\n"
                     "2 for genetic algotitm\n"
                     "3 for ACO \n"
                     "4 for simulated annealing\n"
                     "5 for PSO\n"
                     ))
    lst = []
    if (algo == 1):
        ts = TabuSearch(cvrp, args)
        lst = ts.start()
    if (algo == 2):
        lst = gastart(args, cvrp)
    # if (algo == 3):

    if (algo == 4):
         Simulated_Annealing(cvrp, 100, 0.5, 2048, 1500, 25)
         #cvrp.print_result()
    # if (algo == 5):


    gennumarr = []
    for i in range(len(lst)):
        gennumarr.append(i)
    ax.plot(gennumarr, lst)
    ax.set_title('fitness')

    plt.show()


    #problem = GetInput("\problem1.txt")
    #cv = CVRP(problem.Dimension, problem.Capacity, problem.Cities, problem.Warehouse)
    #mat = cv.Distance_mat()
    #print(mat)
    #Simulated_Annealing(problem, 100, 0.5, 2048, 1500, 25)
    #problem.print_result()