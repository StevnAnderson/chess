from re import I
from .pieces import *
from .board import *
from math import floor, ceil
from sys import exit

class Module:
    gb = Board(8,8)
    turnNum = 0
    turn = 0
    idNum = 0
    kings = list()
    saves = {}
    check = 0

    def __init__(self):
        self.reset()
        self.locateKings()

    def getTeam(self):
        return self.turn

    def visit(self,fun, param=None, piece=None):
        self.gb.visit(fun, param, piece)

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
        self.locateKings()
   
    def clear(self):
        for i in self.gb.grid:
            for j in i:
                if j != 0:
                    self.set(j.getCoor(),0)
        self.locateKings()

    def sq(self, letter):
        match letter:
            case "a":
                return 1
            case "b":
                return 2
            case "c":
                return 3
            case "d":
                return 4
            case "e":
                return 5
            case "f":
                return 6
            case "g":
                return 7
            case "h":
                return 8
            case _:
                return False

    def pc(self, letter):
        if self.turn == 1:
            ret = "W"
        else:
            ret = "B"
        match letter:
            case "R"|"r":
                return ret + "Rook"
            case "N"|"n":
                return ret + "Kght"
            case "B"|"b":
                return ret + "Bshp"
            case "K"|'k':
                return ret + "King"
            case "Q"|'q':
                return ret + "Quen"
            case _:
                return False

    def moveCheckHelper(self,current,d): # p for piece, d for destination
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
                return True
            case "bishop":
                if not p.legalMove(d,target):
                    return False
                deltax = d[0] - p.x()
                deltay = d[1] - p.y()
                if deltax > 0:
                    if deltay > 0:
                        for n in range(1,abs(deltax)):
                            if self.get((p.x()+n, p.y()+n)) != 0:
                                return False
                    else:
                        for n in range(1,abs(deltax)):
                            if self.get((p.x()+n, p.y()-n)) != 0:
                                return False
                else:
                    if deltay > 0:
                        for n in range(1,abs(deltax)):
                            if self.get((p.x()-n, p.y()+n)) != 0:
                                return False
                    else:
                        for n in range(1,abs(deltax)):
                            if self.get((p.x()-n, p.y()-n)) != 0:
                                return False
                return True
            case "knight":
                if not (p.legalMove(d,target)):
                    return False
                return True
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
                return True
                p.Moved()
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
                    return True
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
                                if self.get((p.x()+n, p.y()-n)) != 0:
                                    return False
                    else:
                        if deltay > 0:
                            for n in range(1,deltay):
                                if self.get((p.x()-n, p.y()+n)) != 0:
                                    return False
                        else:
                            for n in range(deltay,-1):
                                if self.get((p.x()-n, p.y()-n)) != 0:
                                    return False
                    return True
            case "king":
                if not (p.legalMove(d,target)):
                    return False
                if abs(p.x() - d[0]) == 2 and p.getMoved()==False:
                    if p.x() < d[0]:
                        xmin = p.x()
                        xmax = 8
                    else:
                        xmin = 1
                        xmax = p.x()
                    for n in range(xmin+1,xmax):
                        if self.get((n,p.y())) != 0:    #Check each square between king and rook
                            return False
                        if self.turn == 1:
                            if self.threatonsWhite((n,p.y())):
                                return False
                        else:
                            if self.threatonsBlack((n,p.y())):
                                return False
                    if xmin == p.x():
                        self.move(self.get((xmax,p.y())), (p.x()+1,p.y()),False)
                        self.move(p, (p.x()+2,p.y()))
                        return
                    else:
                        self.move(self.get((xmin,p.y())), (p.x()-1,p.y()),False)
                        self.move(p, (p.x()-2,p.y()))
                        return
                return True
        
    def moveCheck(self, current,d):
        if self.get(current) != 0 and self.get(current).getTeam() == self.turn and self.moveCheckHelper(current,d):
            self.save("checkChecker")
            self.move(self.gb.get(current),d)
            if self.turn == 2 and self.WhiteCheckStatus():
                self.load("checkChecker")
            elif self.turn == 1 and self.BlackCheckStatus():
                p = self.BlackCheckStatus()
                self.load("checkChecker")
        self.locateKings()

    def textMove(self, text):
        if text.lower() == "exit" or text.lower() == "quit":
            exit()
        if len(text) == 2:
            try:
                if self.turn == 1:
                    self.visit(self.moveCheck,(self.sq(text[0]), int(text[1])), "WPawn")
                else:
                    self.visit(self.moveCheck,(self.sq(text[0]), int(text[1])), "BPawn")
            except:
                return False
            return True
        if len(text) == 3:
            piece = self.pc(text[0])
            collumn = self.sq(text[1])
            row = int(text[2])
            destination = (collumn,row)
            if self.turn == 1:
                tList = self.threatonsBlack(destination)
                difList = [x for x in self.canMove(destination) if x not in tList]
                tList += difList
                tList =list(filter(lambda x: str(x) == piece,tList))
                tList = list(filter(lambda x: x.getTeam() == self.turn, tList))
                if len(tList) > 1:
                    print("Ambiguous move.")
                    return False
                elif len(tList) == 0:
                    return False
                self.moveCheck(tList[0].getCoor(), destination)
            else:
                tList = self.threatonsWhite(destination)
                difList = [x for x in self.canMove(destination) if x not in tList]
                tList += difList
                tList =list(filter(lambda x: str(x) == piece,tList))
                tList = list(filter(lambda x: x.getTeam() == self.turn, tList))
                if len(tList) > 1:
                    print("Ambiguous move.")
                    return False
                elif len(tList) == 0:
                    return False
                self.moveCheck(tList[0].getCoor(), destination)
        if len(text) == 4:
            piece = self.pc(text[0])
            disambig = int()
            DAtype = ""
            try:
                disambig = int(text[1])
                DAtype = 'row' 
            except:
                disambig = self.sq(text[1])
                DAtype = 'collumn'
            collumn = self.sq(text[2])
            row = int(text[3])
            destination = (collumn,row)
            if self.turn == 1:
                tList = self.threatonsBlack(destination)
                tList =list(filter(lambda x: str(x) == piece,tList))
                if len(tList) > 1:
                    if DAtype == row:
                        tList = list(filter(lambda x: x.x() == disambig, tList))
                    else:
                        tList = list(filter(lambda x: x.y() == disambig, tList))
                elif len(tList) == 0:
                    return False
                self.moveCheck(tList[0].getCoor(), destination)
            else:
                tList = self.threatonsWhite(destination)
                tList =list(filter(lambda x: str(x) == piece,tList))
                if len(tList) > 1:
                    print("Ambiguous move.")
                    return False
                elif len(tList) == 0:
                    return False
                self.moveCheck(tList[0].getCoor(), destination)
        self.locateKings()

    def threatonsWhite(self,destination):
        def threatonsHelper(currentCoor, tList):
            tempPiece = self.get(destination)
            self.set(destination, Pawn(self.genID(), 1, destination))
            if self.moveCheckHelper(currentCoor, destination):
                tList.append(self.get(currentCoor))
            self.set(destination, tempPiece)

        threatList = list()
        self.visit(threatonsHelper, threatList)
        return threatList

    def threatonsBlack(self,destination):
        def threatonsHelper(currentCoor, tList):
            tempPiece = self.get(destination)
            self.set(destination, Pawn(self.genID(), 2, destination))
            if self.moveCheckHelper(currentCoor, destination):
                tList.append(self.get(currentCoor))
            self.set(destination, tempPiece)

        threatList = list()
        self.visit(threatonsHelper, threatList)
        return threatList

    def canMove(self, destination):
        def canMoveHelper(currentCoor, tList):
            if self.moveCheckHelper(currentCoor, destination):
                tList.append(self.get(currentCoor))

        threatList = list()
        self.visit(canMoveHelper, threatList)
        return threatList

    def move(self,p,d,tog=True):
        self.gb.set(p.getCoor(),0)
        self.gb.set(d,p)
        p.move(d)
        if tog==True:
            self.toggleTurn()
        self.locateKings()

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
        print("   |   A   |   B   |   C   |   D   |   E   |   F   |   G   |   H   |\n")

    def get(self,c):
        return self.gb.get(c)
    
    def set(self,c,p):
        if p == 0 or (p.x()==c[0] and p.y()==c[1]):
            self.gb.set(c,p)
            self.locateKings()
            return
        else:
             return False
        
    def save(self,name):
        self.gb.save(name)
        self.saves[name] = (self.turn)
    
    def load(self,name):
        if name in self.saves.keys():
            self.gb.load(name)
            self.turn = self.saves[name]
            self.locateKings()
            return True
        return False
    
    def genID(self):
        self.idNum += 1
        return self.idNum
    
    def WhiteCheckStatus(self):
        ret = False
        for k in self.kings:
            if k.getTeam() == 1:
                if self.threatonsWhite(k.getCoor()):
                    ret = True
        return ret        

    def BlackCheckStatus(self):
        ret = False
        for k in self.kings:
            if k.getTeam() == 2:
                if self.threatonsBlack(k.getCoor()):
                    ret = True
        return ret        

    def updateCheck(self):
        pass

    def locateKings(self):
        kings = list()    
        def addKing(k):
            if k !=0:
                if k.character() == "king":
                    kings.append(k)
    
        self.visit(addKing)
        self.kings = kings