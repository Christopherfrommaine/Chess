import threading
from time import time

from side import Side
from move import Move, generateLegalMoves



class Game:
    def __init__(self, lightPlayer, darkPlayer, timeRemaining=(600, 600), timeAdded=(0, 0)):
        self.Pw = lightPlayer
        self.Pb = darkPlayer

        self.timeRemaining = list(timeRemaining)
        self.timeAdded = list(timeAdded)

        self.G = GameState()

        self.running = True
        self.moveGenerationThread = None

        self.Pw.initGame(self, Side('w'))
        self.Pb.initGame(self, Side('b'))

        self.winner = None

    def run(self):
        try:
            while self.running and not self.winner:
                self.update()
        except KeyboardInterrupt:
            self.stopAllThreads()
            self.running = False
        except Exception as e:
            self.stopAllThreads()
            raise e


    def stopAllThreads(self):
        self.moveGenerationThread.join()

    def update(self):
        # Setup search
        self.P.bestMove = None
        self.moveGenerationThread = threading.Thread(target=self.P.generateMove)
        originalTimeRemaining = self.timeRemaining[self.G.turn.i]

        # Starting move generation, while being timed
        startSearchTime = time()
        self.moveGenerationThread.start()

        # Updating display and time remaining
        while self.P.bestMove is None:
            self.Pw.updateDisplay()
            self.Pb.updateDisplay()
            self.timeRemaining[self.G.turn.i] = originalTimeRemaining - (time() - startSearchTime)

        nextMove = self.P.bestMove
        endSearchTime = time()
        self.moveGenerationThread.join()

        self.timeRemaining[self.G.turn.i] = originalTimeRemaining - (endSearchTime - startSearchTime) + self.timeAdded[self.G.turn.i]

        assert isinstance(nextMove, Move)
        self.applyMove(nextMove)

    def applyMove(self, m):
        m.applyToGameState(self.G)

        # Stalemate / Checkmate Check
        if not generateLegalMoves(self.G):
            isCheckmate = False
            Gnew = self.G.copy()
            Gnew.turn = -Gnew.turn
            newLegalMoves = generateLegalMoves(Gnew, False)
            for m in newLegalMoves:
                if Gnew.board[m.end].lower() == 'k':
                    isCheckmate = True
                    break

            if isCheckmate:
                self.win(self.G.turn)
            else:
                # Stalemate Check
                self.win(None)

        # Draw by Repitition check
        repeatedBoardStateCount = 0
        for b in self.G.boardHistory:
            if self.G.board == b:
                repeatedBoardStateCount += 1
        if repeatedBoardStateCount > 3:
            self.win(None)

    def win(self, result):
        print(f'Yippie!! {result} won!')
        self.winner = result

        while self.running:
            self.Pw.updateDisplay()
            self.Pb.updateDisplay()


    @property
    def P(self):
        """Current player"""
        return self.Pw if self.G.turn == 'w' else self.Pb


class GameState:
    """An encaptulation of the current game state, to be used for move exploration."""

    def __init__(self):
        # Current Game State
        self.board = 'rnbqkbnrpppppppp                                PPPPPPPPRNBQKBNR'
        self.canCastle = {'K', 'Q', 'k', 'q'}
        self.turn = Side('w')

        # Game History
        self.boardHistory = [self.board]
        self.moveList = []

    def copy(self):
        o = GameState()

        o.board = self.board  # strings are immutable
        o.canCastle = self.canCastle.copy()
        o.turn = self.turn

        o.boardHistory = self.boardHistory.copy()
        o.moveList = self.moveList.copy()

        return o

    def withMoveApplied(self, m):
        Gcopy = self.copy()
        m.applyToGameState(Gcopy)
        return Gcopy

    @property
    def boardAsList(self):
        return [s for s in self.board]


    # Helper functions for Bots
    def sideValue(self, side):
        peiceToValue = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 11, 'K': 0}
        return sum([peiceToValue[p.upper()] for p in self.board if (p.isupper() if side == 'w' else p.islower())]) + (float('-inf') if ('K' if side == 'w' else 'k') not in self.board else 0)

    def value(self):
        return self.sideValue('w') - self.sideValue('b')

    def isOver(self):
        return not ('k' in self.board and 'K' in self.board)

    def bitboard(self, peiceType):
        o = 0
        for i in range(64):
            o <<= 1
            if self.board[i] == peiceType:
                o += 1
        return o
