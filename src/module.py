from re import I
from .pieces import *
from .board import *
from math import floor, ceil

class Module:
    gb = Board(8,8)
    turnNum = 0
    turn = 0
    idNum = 0

    def __init__(self):
        self.reset()


    def reset(self):
        self.turnNum = 1
        self.turn = 1
        self.gb = Board(8,8)
        self.gb.set((1,1),Rook(self.genID(), 1,(1,1)))
        self.gb.set((2,1),Knight(self.genID(), 1,(2,1)))
        self.gb.set((3,1),Bishop(self.genID(), 1,(3,1)))
        self.gb.set((4,1),Queen(self.genID(), 1,(4,1)))
        self.gb.set((5,1),King(self.genID(), 1,(5,1)))
        self.gb.set((6,1),Bishop(self.genID(), 1,(6,1)))
        self.gb.set((7,1),Knight(self.genID(), 1,(7,1)))
        self.gb.set((8,1),Rook(self.genID(), 1,(8,1)))
        self.gb.set((1,2),Pawn(self.genID(), 1,(1,2)))
        self.gb.set((2,2),Pawn(self.genID(), 1,(2,2)))
        self.gb.set((3,2),Pawn(self.genID(), 1,(3,2)))
        self.gb.set((4,2),Pawn(self.genID(), 1,(4,2)))
        self.gb.set((5,2),Pawn(self.genID(), 1,(5,2)))
        self.gb.set((6,2),Pawn(self.genID(), 1,(6,2)))
        self.gb.set((7,2),Pawn(self.genID(), 1,(7,2)))
        self.gb.set((8,2),Pawn(self.genID(), 1,(8,2)))
        self.gb.set((0,3),0)
        self.gb.set((1,3),0)
        self.gb.set((2,3),0)
        self.gb.set((3,3),0)
        self.gb.set((4,3),0)
        self.gb.set((5,3),0)
        self.gb.set((6,3),0)
        self.gb.set((7,3),0)
        self.gb.set((0,4),0)
        self.gb.set((1,4),0)
        self.gb.set((2,4),0)
        self.gb.set((3,4),0)
        self.gb.set((4,4),0)
        self.gb.set((5,4),0)
        self.gb.set((6,4),0)
        self.gb.set((7,4),0)
        self.gb.set((0,5),0)
        self.gb.set((1,5),0)
        self.gb.set((2,5),0)
        self.gb.set((3,5),0)
        self.gb.set((4,5),0)
        self.gb.set((5,5),0)
        self.gb.set((6,5),0)
        self.gb.set((7,5),0)
        self.gb.set((0,6),0)
        self.gb.set((1,6),0)
        self.gb.set((2,6),0)
        self.gb.set((3,6),0)
        self.gb.set((4,6),0)
        self.gb.set((5,6),0)
        self.gb.set((6,6),0)
        self.gb.set((7,6),0)
        self.gb.set((1,7),Pawn(self.genID(), 2,(1,7)))
        self.gb.set((2,7),Pawn(self.genID(), 2,(2,7)))
        self.gb.set((3,7),Pawn(self.genID(), 2,(3,7)))
        self.gb.set((4,7),Pawn(self.genID(), 2,(4,7)))
        self.gb.set((5,7),Pawn(self.genID(), 2,(5,7)))
        self.gb.set((6,7),Pawn(self.genID(), 2,(6,7)))
        self.gb.set((7,7),Pawn(self.genID(), 2,(7,7)))
        self.gb.set((8,7),Pawn(self.genID(), 2,(8,7)))
        self.gb.set((1,8),Rook(self.genID(), 2,(1,8)))
        self.gb.set((2,8),Knight(self.genID(), 2,(2,8)))
        self.gb.set((3,8),Bishop(self.genID(), 2,(3,8)))
        self.gb.set((4,8),Queen(self.genID(), 2,(4,8)))
        self.gb.set((5,8),King(self.genID(), 2,(5,8)))
        self.gb.set((6,8),Bishop(self.genID(), 2,(6,8)))
        self.gb.set((7,8),Knight(self.genID(), 2,(7,8)))
        self.gb.set((8,8),Rook(self.genID(), 2,(8,8)))


    def moveCheck(self,current,d): # p for piece, d for destination
        p = self.gb.get(current)
        if p == 0:
            return False
        target = self.gb.get(d) # target is the piece at destination
        match p.character():
            case "pawn":
                if not p.legalMove(d,target):
                    return False
                if abs(p.x() - d[0]) == 0: #pawn is moving
                    if (abs(p.y() - d[1]) ==2 and \
                         self.gb.get((p.x(),ceil((p.y() + d[1]) / 2))) != 0): #pawn is moving two spaces
                        return False
                    if self.gb.get((p.x(),d[1])) != 0:
                        return False
                    if abs(p.y() - d[1]) ==1 and \
                         target != 0:
                         return False
                else:   #pawn is attacking
                    if target.getTeam() == p.getTeam():
                        return False
                self.move(p,d)
            case "bishop":
                if not p.legalMove(d,target):
                    return False
                deltax = d[0] - p.x()
                deltay = d[1] - p.y()
                if deltax > 0:
                    if deltay > 0:
                        for n in range(1,deltax):
                            if self.get((p.x()+n, p.y()+n)) != 0:
                                return False
                    else:
                        for n in range(1,deltax):
                            if m.get((p.x()+n, p.y()-n)) != 0:
                                return False
                else:
                    if deltay > 0:
                        for n in range(1,deltax):
                            if m.get((p.x()-n, p.y()+n)) != 0:
                                return False
                    else:
                        for n in range(1,deltax):
                            if m.get((p.x()-n, p.y()-n)) != 0:
                                return False
                self.move(p,d)
            case "knight":
                if not (p.legalMove(d,target)):
                    return False
                self.move(p,d)
            case "rook":
                if not p.legalMove(d,target):
                    return False
                xMin = min(p.getCoor()[0],d[0])
                xMax = max(p.getCoor()[0],d[0])
                yMin = min(p.getCoor()[1],d[1])
                yMax = max(p.getCoor()[1],d[1])
                for n in range(xMin,xMax):
                    if n != d[0] and n != p.getCoor()[0]:
                        if self.gb.get((n,p.getCoor()[1])) != 0:
                            return False
                for n in range(yMin, yMax):
                    if n != d[1] and n != p.getCoor()[1]:
                        if self.gb.get((p.getCoor()[0],n)) != 0:
                            return False
                self.move(p,d)
            case "queen":
                if not p.legalMove(d,target):
                    return False
                if p.x()-d[0] == 0 or p.y()-d[1] == 0:
                    xMin = min(p.getCoor()[0],d[0])
                    xMax = max(p.getCoor()[0],d[0])
                    yMin = min(p.getCoor()[1],d[1])
                    yMax = max(p.getCoor()[1],d[1])
                    for n in range(xMin,xMax):
                        if n != d[0] and n != p.getCoor()[0]:
                            if self.gb.get((n,p.getCoor()[1])) != 0:
                                return False
                    for n in range(yMin, yMax):
                        if n != d[1] and n != p.getCoor()[1]:
                            if self.gb.get((p.getCoor()[0],n)) != 0:
                                return False
                    self.move(p,d)
                else:
                    deltax = d[0] - p.x()
                    deltay = d[1] - p.y()
                    if deltax > 0:
                        if deltay > 0:
                            for n in range(1,deltax):
                                if self.get((p.x()+n, p.y()+n)) != 0:
                                    return False
                        else:
                            for n in range(1,deltax):
                                if m.get((p.x()+n, p.y()-n)) != 0:
                                    return False
                    else:
                        if deltay > 0:
                            for n in range(1,deltax):
                                if m.get((p.x()-n, p.y()+n)) != 0:
                                    return False
                        else:
                            for n in range(1,deltax):
                                if m.get((p.x()-n, p.y()-n)) != 0:
                                    return False
                    self.move(p,d)
            case "king":
                if not (p.legalMove(d,target)):
                    return False
                self.move(p,d)


    def move(self,p,d):
        self.gb.set(p.getCoor(),0)
        self.gb.set(d,p)
        p.move(d)
        self.toggleTurn()


    def toggleTurn(self):
        if self.turn == 1:
            self.turn = 2
            return
        self.turn = 1
        return


    def display(self):
        t = "White" if self.turn == 1 else 2
        print("\n", "Player's Turn:", t, "  Turn Number:", self.turnNum)
        for n in reversed(range(1,9)):
            print(n," | ", end="")
            for m in range(1,9):
                piece = self.gb.get((m,n))
                if piece == 0:
                    print("     ", end=" | ")
                else:
                    print(self.gb.get((m,n)), end=" | ")
            print("\n     --------------------------------------------------------------")
        print("   |   1   |   2   |   3   |   4   |   5   |   6   |   7   |   8   |\n")


    def get(self,c):
        return self.gb.get(c)

    
    def set(self,c,p):
        if p == 0 or (p.x()==c[0] and p.y()==c[1]):
            self.gb.set(c,p)
            return
        else:
             return False

    
    def save(self,name):
        self.gb.save(name)
    

    def load(self,name):
        return self.gb.load(name)
    
    
    def genID(self):
        self.idNum += 1
        return self.idNum