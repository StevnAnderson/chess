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


game = src.module.Module()

while True:
    game.display()
    textMove(input(), game)

