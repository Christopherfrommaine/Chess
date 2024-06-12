from display import DisplaySettings, draw
import pygame
import threading
from random import randint
from move import Move
import time
import numpy as np

class Player:
    def __init__(self, doDisplay=False, displaySettings=DisplaySettings()):
        self.doDisplay = doDisplay
        if self.doDisplay:
            self.displaySettings = displaySettings
        self.pygameEvents = None

        # To be initialized once game is set up
        self.game = None
        self.opponent = None
        self.s = None

    def initGame(self, game, side):
        self.game = game
        self.s = side
        self.opponent = self.game.Pb if self.s == 'w' else self.game.Pw

        if self.doDisplay:
            self.displaySettings.displaySide = self.s.copy()

    def startDisplay(self):
        if self.doDisplay:
            def updateDisplay():
                while self.doDisplay:
                    draw(self)
                    self.handlePygameEvents()

            self.displaySettings.displaySurface = pygame.display.set_mode(self.displaySettings.windowSize)
            self.displaySettings.displayThread = threading.Thread(target=updateDisplay)
            self.displaySettings.displayThread.start()

    def stopDisplay(self):
        if self.doDisplay:
            self.doDisplay = False
            self.displaySettings.displayThread.join()

    def handlePygameEvents(self):
        for event in (newEvents := pygame.event.get()):
            if event.type == pygame.K_RETURN:
                if self.doDisplay:
                    self.stopDisplay()
                else:
                    self.doDisplay = True
                    self.startDisplay()
            if event.type == pygame.K_ESCAPE:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(self.s)
                print(((self.displaySettings.swapIconPos - pygame.mouse.get_pos() + np.array((15, 15))) ** 2).sum())

                # Check for swap display sides
                if ((self.displaySettings.swapIconPos - pygame.mouse.get_pos() + np.array((15, 15))) ** 2).sum() <= 625:
                    self.s = -self.s


        self.pygameEvents = newEvents

    @staticmethod  # To be overwritten by subclasses
    def generateMove():
        time.sleep(1)
        return Move(randint(0, 63), randint(0, 63))


class Bot(Player):
    def __init__(self, maxDepth=3, doDisplay=False, displaySettings=DisplaySettings()):
        Player.__init__(self, doDisplay=doDisplay, displaySettings=displaySettings)
        self.maxDepth = maxDepth
        self.searchThread = None

class Human(Player):
    def __init__(self, displaySettings=DisplaySettings()):
        Player.__init__(self, doDisplay=True, displaySettings=displaySettings)



