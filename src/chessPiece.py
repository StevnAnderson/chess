from .piece import *

class chessPiece(Piece):
    def __init__(self, id, team, coor):
        self.team = team
        self.coor = coor
        self.id = id
        self.moved = False

    def Moved(self):
        self.moved = True
    
    def getMoved(self):
        return self.moved

    def getID(self):
        return self.id


    def x(self):
        return self.coor[0]


    def y(self):
        return self.coor[1]


    def move(self,d):
        self.coor = d
        self.Moved()


    def getCoor(self):
        return self.coor


    def getTeam(self):
        return self.team

        