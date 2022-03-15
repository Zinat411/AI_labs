import random
import numpy as np

W = 0.5
c1 = 0.8
c2 = 0.9
num_iter = 16384
num_particles = 2048

class Particle():
    def __init__(self):
        self.velocity = np.array([0, 0])
        self.position = np.array([(-1) ** (bool(random.getrandbits(1))) * random.random()*50, (-1)**(bool(random.getrandbits(1))) * random.random()*50])
        self.pbest_pos = self.position
        self.pbest_val = float('inf')

    def move(self):
        self.position += self.velocity

class Swarm():
    def __init__(self, target, target_error, n_particles):
        self.target = target
        self.target_error = target_error
        self.n_particles = n_particles
        self.particles = []
        self.gbest_pos = np.array([random.random()*50, random.random()*50])
        self.gbest_val = float('inf')

    def fitness(self, particle):
        return particle.position[0] ** 2 + particle.position[1] ** 2 + 1

    def set_pbest(self):
        for particle in self.particles:
            fitness = self.fitness(particle)
            if(particle.pbest_val > fitness):
                particle.pbest_val = fitness
                particle.pbest_pos = particle.position

    def set_gbest(self):
        for particle in self.particles:
            best_fitness = self.fitness(particle)
            if(self.gbest_val > best_fitness):
                self.gbest_val = best_fitness
                self.gbest_pos = particle.position

    def move_swarm(self):
        for particle in self.particles:
            global W
            new_velocity = (W * particle.velocity) + (c1 * random.random()) * (particle.pbest_pos - particle.position) + \
                           (random.random() * c2) * (self.gbest_pos - particle.position)
            particle.velocity = new_velocity
            particle.move()
