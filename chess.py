import src.module
from enum import Enum



game = src.module.Module()

def textMove(text):
    game.textMove(text)

while True:
    game.display()
    textMove(input())

