from random import randint, random, uniform
import numpy as np



class Particle():
    def __init__(self, position, fitness, velocity, cvrp):
        self.pos_size = len(position)
        self.velocity = velocity
        self.position = position# the particle's string
        self.fitness = fitness
        self.pbest_pos = position
        self.pbest_fitness = fitness
        self.all_dist = cvrp.tour_cost_veh()

    def make_round(self, position):#function to round number to be complete
        for i in range(len(position)):
            position[i] = round(position[i])
        return position

    def move(self, gbest_pos, c1, c2, W):
          gloabl_best = self.all_dist()
          i = c1 * random() * (gloabl_best - self.all_dist(self.position))
          j = c2 * random() * (gloabl_best - self.all_dist(self.position))
          self.velocity = int(self.velocity * random() * W + i + j)
          if self.velocity < 0:
              self.velocity *= -1
          self.velocity = self.velocity % len(self.position)

          for i in range(len(self.position)/2):
              newhold = self.position[i]
              self.position[i] = self.position[(i+self.velocity) % len(self.position)]
              self.position[(i + self.velocity) % len(self.position)] = newhold


    def merge(self, str1, str2):#function to merge two strings
        new_string = []
        for i in range(len(str1)):
            new_string.append((str1[i]) + (str2[i]))
        return new_string

    def pso_str(self, str1, str2, para):#function to create a new string that match pso algorithm
        new_string = []
        for i in range(len(str1)):
            new_string.append((para * ((str1[i]) - (str2[i]))))
        return new_string
    def tour_cost_veh(self, tour, cities):# this function calculates the cost of the vehicle's tour
        matrix = self.Distance_mat()
        count = matrix[tour[0]][0]
        last = len(tour)
        veh_capacity = self.Capacity - self.Cities[tour[0] - 1].demand
        for i in range(last - 1):
            curr = tour[i]
            target = tour[i+1]
            if self.Cities[target-1].demand <= veh_capacity:
                count += matrix[curr][target]
                veh_capacity -= self.Cities[target-1].demand
            else:
                count += matrix[curr][0]
                veh_capacity = self.Capacity - self.Cities[target - 1].demand
                count += matrix[target][0]# new tour for new vehicle starting at target

        count += matrix[tour[last - 1]][0]
        return count

class Swarm():
    def __init__(self, args):
        self.args = args
        self.particles = []
        self.gbest_pos = None
        self.tsize = len(self.args.GA_TARGET)
        self.gbest_fitness = float('inf')
        self.W = 0.5
        self.c1 = 0.8
        self.c2 = 0.9

    def calc_fitness(self, particle):
        str_target = [ord(char) for char in self.args.GA_TARGET]
        fitness = 0
        for i in range(self.tsize):
            fitness += (abs(particle[i] - str_target[i]))
        return fitness

    def sort_by_fitness(self, particles):
        particles.sort(key=lambda i: i.fitness)
        self.gbest_pos = particles[0].position
        self.gbest_fitness = particles[0].fitness

    def initParticles(self):#initilaize the particles array that is indeed the population or the swarm
        for i in range(self.args.GA_POPSIZE):
            velocity = []
            position = []
            for j in range(self.tsize):
                velocity.append(randint(32, 122))
                position.append(randint(32, 122))
            if self.gbest_pos is None:#initilize global best position
               self.gbest_pos = position[0:]
            elif self.calc_fitness(position) < self.calc_fitness(self.gbest_pos):
                self.gbest_pos = position
            particle = Particle(position, self.calc_fitness(position), velocity)
            self.particles.append(particle)
    def to_str(self, gbest_pos):#function to convert to type string
        str = ""
        for i in range(len(gbest_pos)):
            str += chr(gbest_pos[i])
        return str

    def set_pbest(self, fitness, particle):#function to get particle best
            if(particle.pbest_fitness > fitness):
                particle.pbest_fitness = fitness
                particle.pbest_pos = particle.position

    def set_gbest(self, fitness, particle):#function to get global best
            if(self.gbest_fitness > fitness):
                self.gbest_fitness = fitness
                self.gbest_pos = particle.position

    def update_para(self, index, size):#function to update pso parameters
        self.c1 = -3 * (index / size) + 3.5
        self.c2 = 3 * (index / size) + 0.5
        self.W = 0.4 * ((index - size)/ size ** 2) + 0.4



