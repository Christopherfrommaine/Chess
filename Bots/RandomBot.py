import time
from random import choice
from time import sleep

from player import Player
from move import generateLegalMoves


class Bot(Player):
    def __init__(self, doDisplay=False, timePerMove=0):
        Player.__init__(self, doDisplay=doDisplay)
        self.timePerMove = timePerMove

    def generateMove(self):
        sleep(self.timePerMove)
        self.bestMove = choice(generateLegalMoves(self.game.G))
