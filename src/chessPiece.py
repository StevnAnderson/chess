from numpy import kaiser
from .piece import *

class chessPiece(Piece):
    def __init__(self, id, team, coor):
        self.team = team
        self.coor = coor
        self.id = id


    def getID(self):
        return self.id


    def x(self):
        return self.coor[0]


    def y(self):
        return self.coor[1]


    def move(self,d):
        self.coor = d


    def getCoor(self):
        return self.coor


    def getTeam(self):
        return self.team

        