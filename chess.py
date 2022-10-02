import src.module
from enum import Enum

def textMove(text, game):
    if len(text) == 2:
        try:
            if game.turn == 1:
                game.visit(game.moveCheck,(sq(text[0]), int(text[1])), "WPawn")
            else:
                game.visit(game.moveCheck,(sq(text[0]), int(text[1])), "BPawn")
        except:
            return False
        return True
    if len(text) == 3:
        piece = pc(text[0])
        collumn = sq(text[1])
        row = int(text[2])
        destination = (collumn,row)
        if game.turn == 1:
            tList = game.threatonsBlack(destination)
            tList =list(filter(lambda x: str(x) == piece,tList))
            if len(tList) > 1:
                print("Ambiguous move.")
                return False
            elif len(tList) == 0:
                return False
            game.moveCheck(tList[0].getCoor(), destination)
        else:
            tList = game.threatonsWhite(destination)
            tList =list(filter(lambda x: str(x) == piece,tList))
            if len(tList) > 1:
                print("Ambiguous move.")
                return False
            elif len(tList) == 0:
                return False
            game.moveCheck(tList[0].getCoor(), destination)
                
            
def sq(letter):
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

def pc(letter):
    if game.turn == 1:
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

game = src.module.Module()

while True:
    game.display()
    textMove(input(), game)

