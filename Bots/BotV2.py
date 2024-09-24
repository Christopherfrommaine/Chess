from random import choice

from player import Player
from move import generateLegalMoves


class Bot(Player):
    def __init__(self, maxDepth=3, doDisplay=False):
        Player.__init__(self, doDisplay=doDisplay)
        self.maxDepth = maxDepth
        self.nodesSearched = 0

    def minimax(self, G, depth=0, alpha=float('-inf'), beta=float('inf')):
        self.nodesSearched += 1

        if G.isOver() or depth >= self.maxDepth:
            return G.value()

        if G.turn == 'w':
            bestValue = float('-inf')
            for m in generateLegalMoves(G, False):
                bestValue = max(bestValue, self.minimax(G.withMoveApplied(m), depth + 1, alpha, beta))
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestValue

        if G.turn == 'b':
            bestValue = float('inf')
            for m in generateLegalMoves(G, False):
                bestValue = min(bestValue, self.minimax(G.withMoveApplied(m), depth + 1, alpha, beta))
                beta = min(beta, bestValue)
                if beta <= alpha:
                    break
            return bestValue

    def generateMove(self):
        G = self.game.G

        alpha = float('-inf')
        beta = float('inf')

        bestMove = None
        legalMoves = generateLegalMoves(G, False)

        if self.s == 'w':
            bestValue = float('-inf')
            for m in legalMoves:
                nextValue = self.minimax(G.withMoveApplied(m), 0, alpha, beta)

                if nextValue > bestValue:
                    bestValue = nextValue
                    bestMove = m

                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break

        if self.s == 'b':
            bestValue = float('inf')
            for m in legalMoves:
                nextValue = self.minimax(G.withMoveApplied(m), 0, alpha, beta)

                if nextValue < bestValue:
                    bestValue = nextValue
                    bestMove = m
                beta = min(beta, bestValue)
                if beta <= alpha:
                    break

        self.nodesSearched = 0

        self.bestMove = bestMove if bestMove is not None else choice(legalMoves)
