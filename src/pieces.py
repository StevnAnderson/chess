from .chessPiece import *
bounds = []
for n in range(1,9):
    for m in range(1,9):
        bounds.append((m,n))

#Needs promotion coded
class Pawn(chessPiece):

    def legalMove(self, destination, destinationOccupancy):
        if destination not in bounds:
            return False
        if self.team == 2:
            if self.coor[0] - destination[0] == 0 and self.coor[1] - destination[1] == 1 and destinationOccupancy == 0:
                if destination[1] == 1:
                    self.promotion(self)
                return True
            if self.coor[0] - destination[0] == 0 and self.coor[1] - destination[1] == 2 and destinationOccupancy == 0 and \
                self.getCoor()[1] == 7:
                if destination[1] == 1:
                    self.promotion(self)
                return True
            if abs(self.coor[0] - destination[0]) == 1 and self.coor[1] - destination[1] == 1 and destinationOccupancy.getTeam() == 1:
                if destination[1] == 1:
                    self.promotion(self)
                return True
        if self.team == 1:
            if self.coor[0] - destination[0] == 0 and self.coor[1] - destination[1] == -1 and destinationOccupancy == 0:
                return True
            if self.coor[0] - destination[0] == 0 and self.coor[1] - destination[1] == -2 and destinationOccupancy == 0 and \
                self.getCoor()[1] == 2:
                return True
            if abs(self.coor[0] - destination[0]) == 1 and self.coor[1] -destination[1] == -1 and destinationOccupancy != 0 and destinationOccupancy.getTeam() == 2:
                return True
        return False

    
    def promotion(self):
        pass

    def __str__(self) -> str:
        if self.team == 1:
            return "WPawn"
        return "BPawn"

    def character(self):
        return "pawn"

    
class King(chessPiece):
    def legalMove(self, destination, destinationOccupancy):
        if self.moved == False:
            if abs(destination[0] - self.x()) == 2 and self.y() - destination[1] == 0:
                return True                
        if destination not in bounds:
            return False
        if destinationOccupancy != 0 and destinationOccupancy.getTeam() == self.getTeam():
            return False
        if not(abs(self.coor[0] - destination[0]) < 2 and abs(self.coor[1] - destination[1]) < 2):
            return False
        return True

    def __str__(self):
        if self.team == 1:
            return "WKing"
        return "BKing"

    def character(self):
        return "king"
    

class Queen(chessPiece):
    def __str__(self) -> str:
        if self.team == 1:
            return "WQuen"
        return "BQuen"
    
    
    def legalMove(self,destination, destinationOccupancy):
        if destination not in bounds:
            return False
        if destinationOccupancy != 0 and destinationOccupancy.getTeam() == self.getTeam():
            return False
        if self.coor[0] - destination[0] == 0 or \
            self.coor[1] - destination[1] == 0 or \
            abs(self.coor[0] - destination[0]) == abs(self.coor[1]-destination[1]):
            return True
        return False

    def character(self):
        return "queen"

    
class Bishop(chessPiece):
    def __str__(self)->str:
        if self.team == 1:
            return "WBshp"
        return "BBshp"
    
    def legalMove(self,destination, destinationOccupancy):
        if destination not in bounds:
            return False
        if not (abs(self.coor[0] - destination[0]) == abs(self.coor[1] - destination[1])):
            return False
        if destinationOccupancy != 0 and destinationOccupancy.getTeam() == self.getTeam():
            return False
        return True
    
    def character(self):
        return "bishop"


class Knight(chessPiece):
    def __str__(self)->str:
        if self.team == 1:
            return "WKght"
        return "BKght"

    def legalMove(self, destination, destinationOccupancy):
        if destination not in bounds:
            return False
        if destinationOccupancy != 0 and destinationOccupancy.getTeam() == self.getTeam():
            return False
        if not((abs(self.coor[0] - destination[0]) == 2 and abs(self.coor[1] - destination[1]) == 1) or\
            (abs(self.coor[1] - destination[1]) == 2 and abs(self.coor[0] - destination[0]) == 1)):
            return False
        return True

    def character(self):
        return "knight"


class Rook(chessPiece):
    def __str__(self)->str:
        if self.team == 1:
            return "WRook"
        return "BRook"
    
    def legalMove(self,destination, destinationOccupancy):
        if destination not in bounds:
            return False
        if destinationOccupancy != 0 and destinationOccupancy.getTeam() == self.getTeam():
            return False
        if not (self.getCoor()[0] - destination[0] == 0 or self.getCoor()[1] - destination[1] == 0):
            return False                
        return True
    
    def character(self):
        return "rook"
