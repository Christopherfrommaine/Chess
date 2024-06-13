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

        self.timeRemaining = list(timeRemaining)
        self.timeAdded = list(timeAdded)

        self.running = True

        self.moveGenerationThread = None

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
        self.moveGenerationThread.join()

    def update(self):
        # Setup search
        self.P.bestMove = None
        self.moveGenerationThread = threading.Thread(target=self.P.generateMove)
        originalTimeRemaining = self.timeRemaining[self.G.turn.i]

        # Starting move generation, while being timed
        startSearchTime = time.time()
        self.moveGenerationThread.start()

        # Updating display and time remaining
        while self.P.bestMove is None:
            self.Pw.updateDisplay()
            self.Pb.updateDisplay()
            self.timeRemaining[self.G.turn.i] = originalTimeRemaining - (time.time() - startSearchTime)

        nextMove = self.P.bestMove
        endSearchTime = time.time()
        self.moveGenerationThread.join()

        self.timeRemaining[self.G.turn.i] = originalTimeRemaining - (endSearchTime - startSearchTime) + self.timeAdded[self.G.turn.i]

        assert isinstance(nextMove, Move)
        nextMove.applyToGameState(self.G)

    @property
    def P(self):
        """Current player"""
        return self.Pw if self.G.turn == 'w' else self.Pb


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
        self.boardHistory = [self.board]
        self.moveList = []

    @property
    def boardAsList(self):
        return [s for s in self.board]

