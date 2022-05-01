from lab3.CVRP import CVRP
from lab3.City import City



def GetInput(name):
        file = open(r"C:\Users\WIN10\Desktop\CVRP\CVRP\problem1.txt")
        file.readline()
        file.readline()
        file.readline()
        line=file.readline()
        words = line.split()
        dimension=int(words[2])
        file.readline()
        line = file.readline()
        words = line.split()
        capacity=int(words[2])
        file.readline()
        citylst=[]
        i=0
        for l in range(dimension):
            line = file.readline()
            words = line.split(' ')
            city=City(int(words[0]) ,int(words[1]),int(words[2]))
            citylst.append(city)
        file.readline()
        for l in range(dimension):
            line = file.readline()
            words = line.split(' ')
            citylst.__getitem__(i).setDemand(int(words[1]))
            i += 1

        warehouse=citylst.__getitem__(0)
        citylst.__delitem__(0)
        citylst.insert(0, warehouse)
        cvrp=CVRP(dimension,capacity,citylst,warehouse)
        #print(citylst[2].Xcor)
        return cvrp

