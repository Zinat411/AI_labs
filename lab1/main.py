import time
from Genetic5 import *
from Arguments import *
from Struct import *
from Functions import *
from timeit import default_timer as timer
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

def run(ga, population, buffer, args1, esize):
    start_qt = time.time()  # the start time of clock ticks
    start_elapsed = timer()  # the start time of elapsed
    for i in range(args1.GA_MAXITER):
        iteration_time = time.time()
        ga.calc_fitness(population)
        #bull_hits(population, args1)
        ga.sort_by_fitness(population)
        ga.print_best(population)
        avgfitness = ga.calc_avg_fitness(population)
        print("The average of the fitness is:", avgfitness)
        standard_dv = ga.calc_SD(population, avgfitness)
        print("The standard deviation is: ", standard_dv)
        if population[0].getFitness() == 0:
            print()
            print("Best string: " + population[0].str)
            print(f'found in {i} iterations out of {args1.GA_MAXITER}')
            norm_fitness = normalize(population, args1)
            histogram(norm_fitness, population, args1)
            break
        ga.mate(population, buffer)
        clock_ticks = time.time() - iteration_time
        print("Clock ticks time: ", clock_ticks)
        population, buffer = buffer, population
    elapsed_time = timer() - start_elapsed
    print("Elapsed time: ", elapsed_time)
def single():
    GArun("Single")

def two():
    GArun("Two")

def uniform():
    GArun("Uniform")

def GArun(cross_type):
    args1 = get_input()
    if (cross_type == "Single"):
        args1.CROSS_TYPE = "Single"
    elif (cross_type == "Two"):
        args1.CROSS_TYPE = "Two"
    elif(cross_type == "Uniform"):
        args1.CROSS_TYPE = "Uniform"
    ga = Genetic5(args1)
    print("Cross type:", args1.CROSS_TYPE)
    esize = int(args1.GA_POPSIZE * args1.GA_ELITRATE)
    pop_alpha = [None] * args1.GA_POPSIZE
    pop_beta = [None] * args1.GA_POPSIZE
    ga.init_population(pop_alpha, pop_beta)
    population = pop_alpha
    buffer = pop_beta
    run(ga, population, buffer, args1, esize)


def get_input():
    popsize = int(ENTRIES[0].get())
    maxIter = int(ENTRIES[1].get())
    eliteRate = float(ENTRIES[2].get())
    mutationRate = float(ENTRIES[3].get())
    targetString = str(ENTRIES[4].get())
    cross_type = str(ENTRIES[5].get())
    args = Var(popsize, maxIter, eliteRate, mutationRate, targetString, cross_type)
    return args

if __name__ == '__main__':
    root = Tk()
    root.title("Ai Lab 1")
    root.configure(background='#2b2b2b')
    root.geometry("800x900")  # width X height
    root.resizable(False, False)
    #Label(root, text="Please choose crossover type:", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=8,padx=10,pady=10)
    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)
    e4 = Entry(root)
    e5 = Entry(root)
    e6 = Entry(root)
    ENTRIES.append(e1)
    ENTRIES.append(e2)
    ENTRIES.append(e3)
    ENTRIES.append(e4)
    ENTRIES.append(e5)
    ENTRIES.append(e6)
    e1.insert(END, '2048')
    e2.insert(END, '16384')
    e3.insert(END, '0.1')
    e4.insert(END, '0.5')
    e5.insert(END, 'Hello World!')
    e6.insert(END, 'Single')
    #e1.grid(row=0, column=1)
    #e2.grid(row=1, column=1)
    #e3.grid(row=2, column=1)
    #e4.grid(row=3, column=1)
    #e5.grid(row=4, column=1)
    Button(root, text="Run Genetic Algorithm", command=single, bg='#3c3f41', fg='#a9b7c6', bd=0,
           font=("JetBrains Mono", 18)).grid(row=4, column=2, padx=10, pady=10)
    #Button(root, text="Single Point Crossover", command=GArun("Single"), bg='#3c3f41', fg='#a9b7c6', bd=0,font=("JetBrains Mono", 18)).grid(row=9, padx=10,pady=10)
    Button(root, text="Two Point Crossover", command=two, bg='#3c3f41', fg='#a9b7c6', bd=0,font=("JetBrains Mono", 18)).grid(row=10, padx=10,pady=10)
    Button(root, text="Uniform Crossover", command=uniform, bg='#3c3f41', fg='#a9b7c6', bd=0,font=("JetBrains Mono", 18)).grid(row=11, padx=10,pady=10)

    root.mainloop()
