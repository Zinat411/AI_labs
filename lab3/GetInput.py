from lab3.CVRP import CVRP
from lab3.City import City
import math

def GetInput(name):
        file = open(r"C:\Users\WIN10\Desktop\CVRP\CVRP\problem1.txt")
        file.readline()
        file.readline()
        file.readline()
        line=file.readline()
        words = [index for index in line.split(' ')]
        dimension=int(words[2])
        file.readline()
        line2 = file.readline()
        words = [index for index in line2.split(' ')]
        capacity = int(words[2])
        file.readline()
        line3 = file.readline()
        words = [index for index in line3.split(' ')]
        warehouse = City(int(words[0]),int(words[1]),int(words[2]))
        citylst=[]
        i=0
        for l in range(dimension - 1):
            line4 = file.readline()
            words = words = [index for index in line4.split(' ')]
            city=City(int(words[0]) - 1,int(words[1]),int(words[2]))
            citylst.append(city)
        file.readline()
        file.readline()
        for i in range(dimension - 1):
            line5 = file.readline()
            words = [index for index in line5.split(' ')]
            citylst[i].setDemand(int(words[1]))

        citylst.insert(0, warehouse)
        matrix = Distance_mat(citylst)
        citylst.pop(0)
        print('the size',len(citylst) )
        #for i in range(len(citylst)):
            #print('city', citylst[i].id, citylst[i].Xcor)
        cvrp=CVRP(dimension,capacity,citylst,warehouse, matrix)
        #matrix = cvrp.Distance_mat()

        #print(citylst[2].Xcor)
        return cvrp

def Distance_mat(citylst):
        numCities = len(citylst)
        rows, cols = numCities, numCities
        arr_row = []
        for i in range(rows):
            arr_col = []
            for j in range(cols):
                dx = (citylst[i].Xcor - citylst[j].Xcor) * (citylst[i].Xcor - citylst[j].Xcor)
                dy = (citylst[i].Ycor - citylst[j].Ycor) * (citylst[i].Ycor - citylst[j].Ycor)
                distance = math.sqrt(dx + dy)
                arr_col.append(distance)
            arr_row.append(arr_col)
        return arr_row