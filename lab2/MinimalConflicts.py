import random
import Struct
import sys
from Struct import Struct
import numpy as np
import numpy as np
from Nqueens import *

class MinimalConflicts:
    def __init__(self, args):
        self.args = args
        self.nqueens = args.nqueens
        self.board=[int]*self.nqueens

    def checkCflict(self,board):

        count=0
        for i in range(self.nqueens):

            for j in range(self.nqueens):
                if i!=j:
                   conflict=self.canQueenAttack(i+1,self.board[i],j+1,self.board[j])
                   if conflict==True:
                       count+=1
        return count



    def init(self):

        min=100*self.nqueens
        newval=0
        connum=0
        for i in range(self.nqueens):
            self.board[i]=random.randrange(self.nqueens)
        for i in range(1000):
            min = 100 * self.nqueens
            index = random.randrange( self.nqueens)
            for i in range(self.nqueens):
                self.board[index]=i
                connum= self.checkCflict(self.board)
                if connum<min:
                    min=connum
                    newval=i

            self.board[index]=newval
            if min==0:
                break
        print("board is: ",self.board)
        return 0

    def canQueenAttack(self, qR, qC, oR, oC):

        # If queen and the opponent are
        # in the same row
        if qR == oR:
            return True

        # If queen and the opponent are
        # in the same column
        if qC == oC:
            return True

        # If queen can attack diagonally
        if abs(qR - oR) == abs(qC - oC):
            return True

        # Opponent is safe
        return False

