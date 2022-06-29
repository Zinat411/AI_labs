


class Agent:
    def __init__(self,arr,fitness,network):
         self.arr=arr
         self.fitness=fitness
         self.age = 0
         self.network=network
         self.reg = 0