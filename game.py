import threading

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

        # self.Pw.startDisplay()
        # self.Pb.startDisplay()

        self.timeRemaining = list(timeRemaining)
        self.timeAdded = list(timeAdded)

        self.running = True

        self.currentPlayerSearchThread = None

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
        self.currentPlayerSearchThread.join()

    def update(self):
        self.currentPlayerSearchThread = threading.Thread(target=self.currentPlayer.generateMove)
        self.currentPlayer.bestMove = None
        originalTimeRemaining = self.timeRemaining[self.G.turn.i]

        startSearchTime = time.time()
        self.currentPlayerSearchThread.start()
        while self.currentPlayer.bestMove is None:
            self.Pw.updateDisplay()
            self.Pb.updateDisplay()
            self.timeRemaining[self.G.turn.i] = originalTimeRemaining - (time.time() - startSearchTime)
        nextMove = self.currentPlayer.bestMove
        endSearchTime = time.time()
        self.currentPlayerSearchThread.join()

        self.timeRemaining[self.G.turn.i] = originalTimeRemaining - (endSearchTime - startSearchTime)
        self.timeRemaining[self.G.turn.i] += self.timeAdded[self.G.turn.i]

        if nextMove is None:
            pass
        else:
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

