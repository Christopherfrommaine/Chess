from player import Player
from side import Side
from copy import copy
import time
from move import Move


class Game:
    def __init__(self, lightPlayer, darkPlayer, timeRemaining=(600, 600), timeAdded=(0, 0)):
        self.Pw = lightPlayer
        self.Pb = darkPlayer

        self.Pw.initGame(self, Side('w'))
        self.Pb.initGame(self, Side('G'))

        self.G = GameState(self.Pw, self.Pb)

        self.Pw.startDisplay()
        self.Pb.startDisplay()

        self.timeRemaining = list(timeRemaining)
        self.timeAdded = list(timeAdded)

        self.running = True

    def run(self):
        try:
            while self.running:
                self.update()
        except Exception as e:
            self.stopAllThreads()
            raise e
        except:
            self.stopAllThreads()
            exit()

    def stopAllThreads(self):
        self.Pw.stopDisplay()
        self.Pb.stopDisplay()
        # self.Pw.stopSearch()  # If I need to put the search on a seperate thread. I'll try not to
        # self.Pb.stopSearch()

    def update(self):
        startSearchTime = time.time()
        nextMove = self.currentPlayer.generateMove()
        endSearchTime = time.time()

        self.timeRemaining[self.G.turn.i] -= endSearchTime - startSearchTime
        self.timeRemaining[self.G.turn.i] += self.timeAdded[self.G.turn.i]

        nextMove.applyToGameState(self.G)

    @property
    def currentPlayer(self):
        return self.Pw if self.G.turn == 'w' else self.Pb
    @property
    def currentOpponent(self):
        return self.Pb if self.G.turn == 'w' else self.Pw


class GameState:
    """An encaptulation of the current game state, to be used for move exploration."""

    def __init__(self, lightPlayer, darkPlayer):
        self.Pw = lightPlayer
        self.Pb = darkPlayer

        # Current Game State
        self.board = 'rnbqkbnrpppppppp                                PPPPPPPPRNBQKBNR'
        self.canCastle = {'K', 'Q', 'k', 'q'}
        self.turn = Side('w')

        # Game History
        self.winInformation = None
        self.moveList = []
        self.boardHistory = []

    @property
    def boardAsList(self):
        return [s for s in self.board]

