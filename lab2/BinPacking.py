from Bins import Bins
import random
import sys
class BinPacking:
    def __init__(self,args):
        self.args=args
        self.tsize=len(args.weightarr)
        self.esize=int(self.args.GA_POPSIZE * self.args.GA_ELITRATE)
        self.numBins=args.numBins
        self.weightarr=args.weightarr
        self.binsize=args.binsize

    def initpop(self,population: list[Bins], buffer: list):
        for i in range(self.args.GA_POPSIZE):
             temp=[int]*self.tsize
             fitness1 = 0
             for j in range(self.tsize):
                 temp[j] = random.randrange(self.numBins)

             population[i]=Bins(temp,fitness1)



    def calc_fitness(self,population:list[Bins]):
        for i in range(self.args.GA_POPSIZE):
            arr=[int]*self.numBins
            sizesum = 0
            weightsum = 0
            for j in range(self.numBins):
                arr[j]=0
            for j in range(self.numBins):
                x=int(population[i].arr[j]-1)
                arr[x]+=self.weightarr[j]

            for j in range(self.numBins):
                if arr[j]>self.binsize[j]:
                    population[i].fitness=100
                    break
            weightsum = sum(arr)
            sizesum = sum(self.binsize)
            population[i].fitness = 100 - int(weightsum / sizesum)

    def sort_by_fitness(self, population: list[Bins]):
        population.sort(key=lambda i: i.fitness)

    def elitism(self, population: list[Bins], buffer: list[Bins]):
        temp = population[:self.esize].copy()
        buffer[:self.esize] = temp

    def mate(self,population:list[Bins],buffer:list[Bins]):
        self.elitism(population, buffer)
        for i in range(self.esize, self.args.GA_POPSIZE):
            i1 = random.randint(0, (self.args.GA_POPSIZE / 2) - 1)
            i2 = random.randint(0, (self.args.GA_POPSIZE / 2) - 1)

            spos = random.randint(0, self.tsize - 1)
            if (self.args.CROSS_TYPE == "Single"):
                buffer[i] = Bins(population[i1].arr[0: spos] + population[i2].arr[spos:], 0)
            if (self.args.CROSS_TYPE == "Two"):
                spos1 = random.randint(0, self.tsize - 2)
                spos2 = random.randint(spos1 + 1, self.tsize - 1)
                buffer[i] = Bins(
                    population[i1].arr[0: spos1] + population[i2].arr[spos1:spos2] + population[i1].arr[spos2:], 0)
            if (self.args.CROSS_TYPE == "Uniform"): # there is a chance uniform wont work
                gene = ""
                for j in range(self.tsize):
                    x = random.randint(0, sys.maxsize) % 2
                    if x == 0:
                        gene = gene + population[i1].arr[j]
                    else:
                        gene = gene + population[i2].arr[j]
                buffer[i] = Bins(gene, 0)
            if random.random() < self.args.GA_MUTATION:
                self.mutate(buffer[i])




    def mutate(self, member: Bins):
        ipos = random.randint(0, self.tsize - 1)

        member.arr[ipos]=member.arr[ipos]/2


    def print_best(self, gav: list[Bins]):
        print('Best: ', gav[0].arr, '(', str(gav[0].fitness), ')')