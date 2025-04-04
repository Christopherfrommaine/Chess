from display import DisplaySettings, draw
import pygame
from random import randint
from move import moveFromTuple, generateLegalMoves, moveToTuple
import time
import numpy as np

class Player:
    def __init__(self, doDisplay=False, displaySettings=DisplaySettings()):
        self.doDisplay = doDisplay
        if self.doDisplay:
            self.displaySettings = displaySettings
        self.pygameEvents = None

        # For searching
        self.bestMove = None

        # To be initialized once game is set up
        self.game = None
        self.opponent = None
        self.s = None

    def initGame(self, game, side):
        self.game = game
        self.s = side
        self.opponent = self.game.Pb if self.s == 'w' else self.game.Pw

        if self.doDisplay:
            self.displaySettings.displaySide = self.s
            self.displaySettings.displaySurface = pygame.display.set_mode(self.displaySettings.windowSize)

    def updateDisplay(self):
        if self.doDisplay:
            draw(self)
            self.handlePygameEvents()

    def handlePygameEvents(self):
        newEvents = pygame.event.get()
        for event in newEvents:
            if event.type == pygame.K_ESCAPE or event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check for swap display sides
                if ((self.displaySettings.swapIconPos - pygame.mouse.get_pos() + np.array((15, 15))) ** 2).sum() <= 625:
                    self.s = -self.s
        self.pygameEvents = newEvents

    def generateMove(self):  # To be overwritten by subclasses
        time.sleep(1 + self.s.i)
        allMoves = generateLegalMoves(self.game.G)
        self.bestMove = allMoves[randint(0, len(allMoves) - 1)]


class Bot(Player):
    def __init__(self, doDisplay=False, displaySettings=DisplaySettings()):
        Player.__init__(self, doDisplay=doDisplay, displaySettings=displaySettings)


class Human(Player):
    def __init__(self, displaySettings=DisplaySettings()):
        Player.__init__(self, doDisplay=True, displaySettings=displaySettings)
        self.selected = None
        self.selectedLegalMoves = None

    def handlePygameEvents(self):
        newEvents = pygame.event.get()
        for event in newEvents:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_F2:
                    self.game.running = False
                if event.key == pygame.K_RETURN:
                    self.displaySettings.displaySide = -self.displaySettings.displaySide

                # Change index for looking at game history with left or right arrow keys
                if event.key == pygame.K_LEFT:
                    if self.displaySettings.displayMoveHistory is None:
                        self.displaySettings.displayMoveHistory = len(self.game.G.boardHistory) - 2
                    else:
                        self.displaySettings.displayMoveHistory -= self.displaySettings.displayMoveHistory > 0
                if event.key == pygame.K_RIGHT:
                    if self.displaySettings.displayMoveHistory is not None:
                        self.displaySettings.displayMoveHistory += 1
                        if self.displaySettings.displayMoveHistory >= len(self.game.G.boardHistory) - 1:
                            self.displaySettings.displayMoveHistory = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = np.array(pygame.mouse.get_pos())

                # Swap Display Sides
                if ((self.displaySettings.swapIconPos - mpos + np.array((15, 15))) ** 2).sum() <= 625:
                    self.displaySettings.displaySide = -self.displaySettings.displaySide

                # Click the board to move peices
                elif (self.displaySettings.borderSize <= mpos).all() and (mpos <= (self.displaySettings.windowSize - self.displaySettings.borderSize)).all():
                    mcoords = (mpos - self.displaySettings.borderSize) // self.displaySettings.tileSize
                    self.clickBoard(mcoords)
        self.pygameEvents = newEvents

    def clickBoard(self, mcoords):
        if self.displaySettings.displaySide == 'b':
            mcoords[1] = 7 - mcoords[1]
            mcoords[0] = 7 - mcoords[0]

        mi = int(mcoords.dot((1, 8)))
        
        if self.selected is not None and mi in self.displaySettings.highlightedTiles:
            self.bestMove = moveFromTuple((self.selected, mi))

        self.displaySettings.highlightedTiles = []

        self.selected = mi if (self.s == 'w' and self.game.G.board[mi].isupper()) or (self.s == 'b' and self.game.G.board[mi].islower()) else None

        if self.bestMove is None:
            self.displaySettings.highlightedTiles = [moveToTuple(m)[1] for m in generateLegalMoves(self.game.G) if moveToTuple(m)[0] == self.selected]

    def generateMove(self):
        # Move generation is done through interacting with the board.
        self.bestMove = None
        self.displaySettings.highlightedTiles = []
