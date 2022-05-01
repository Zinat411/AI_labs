
class City:
    def __init__(self,id, Xcor, Ycor):
        self.id = id
        self.Xcor= Xcor
        self.Ycor = Ycor
        self.demand = 0

    def setDemand(self, demand):
        self.demand = demand

