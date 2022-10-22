from numpy import float64
import src.module

game = src.module.Module()

def textMove(text):
    game.textMove(text)

while True:
    game.display()
    textMove(input())
float