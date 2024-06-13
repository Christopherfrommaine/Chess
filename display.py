import time

import pygame
import numpy as np
from side import Side

pygame.init()
try:
    fontPath = pygame.font.match_font('microsoftsansserif')
except Exception:
    fontPath = pygame.font.get_default_font()
imageCache = {}

class DisplaySettings:
    """Object to hold all of the information about displaying the chess board. Fully customizable when initializing Player class."""
    def __init__(self, windowSize=(1280, 720), tileSize=60, timeTextSize=24, lightColor=(191, 131, 80), darkColor=(128, 78, 37), highlightColor=(200, 200, 0), clickedColor=(200, 100, 100), timeTextColor=(255, 255, 255), timeTextActiveBackgroundColor=(50, 50, 50), timeTextInactiveBackgroundColor=(100, 100, 100)):
        self.displaySurface = None
        self.displayMoveHistory = None
        self.displaySide = None

        self.windowSize = np.array(windowSize)
        self.tileSize = tileSize
        self.timeTextSize = timeTextSize
        self.borderSize = np.array(((self.windowSize[0] - 8 * self.tileSize) * 0.5, (self.windowSize[1] - 8 * self.tileSize) * 0.5))
        self.swapIconPos = self.windowSize - self.borderSize + np.array((10, -40))  # Lower right of board

        self.lightColor = lightColor
        self.darkColor = darkColor
        self.highlightColor = highlightColor
        self.clickedColor = clickedColor
        self.timeTextColor = timeTextColor
        self.timeTextActiveBackgroundColor = timeTextActiveBackgroundColor
        self.timeTextInactiveBackgroundColor = timeTextInactiveBackgroundColor

    def sideColor(self, s):
        """Returns the correct tile color for a specific side."""
        if Side('w') == s:
            return self.lightColor
        if Side('G') == s:
            return self.darkColor

    def textBackgroundColor(self, player, side):
        """Returns either active or inactive background color."""
        return self.timeTextActiveBackgroundColor if side != player.game.G.turn else self.timeTextInactiveBackgroundColor


def draw(player):
    S = player.displaySettings
    window = S.displaySurface
    side = S.displaySide
    b = player.game.G.board if S.displayMoveHistory is None else player.game.G.boardHistory[S.displayMoveHistory]

    window.fill(0)

    for i in range(64):
        coords = np.array((i % 8, i // 8))  # Tile coordinates on board
        if side == 'b':
            coords = 7 - coords

        tilePos = (S.tileSize * coords) + S.borderSize  # Tile position on display

        # Draw Tile
        tileColor = S.sideColor(1 - (coords.sum() % 2))
        if hasattr(player, 'selected'):
            if i == player.selected:
                tileColor = 0.2 * np.array(tileColor) + 0.8 * np.array(S.clickedColor)
        pygame.draw.rect(window, tileColor, pygame.Rect(*tilePos, S.tileSize, S.tileSize))

        # Draw Peice
        if (peice := b[i]) != ' ':
            path = ('1' if peice.isupper() else '0') + str(peice).lower()
            window.blit(getImageData(path), tilePos)

    # Get Time Text Font
    font = pygame.font.Font(fontPath, S.timeTextSize)
    padding = S.timeTextSize // 3

    # Display Time Text:
    for side in (player.s, -player.s):
        timeText = font.render(formatAsTime(player.game.timeRemaining[side.i]), True, S.timeTextColor)
        rs = np.array(timeText.get_size())
        if side == player.s:
            textPos = np.array((S.borderSize[0] - rs[0] - 2 * padding, S.windowSize[1] - S.borderSize[1] - S.timeTextSize - padding))
        else:
            textPos = np.array((S.borderSize[0] - rs[0] - 2 * padding, S.borderSize[1] + S.timeTextSize - rs[1] + padding))
        backgroundRect = pygame.rect.Rect(*(textPos - padding), *(rs + 2 * padding))
        pygame.draw.rect(window, S.textBackgroundColor(player, side), backgroundRect)
        window.blit(timeText, textPos)

    # Display Swap Icon
    window.blit(getImageData('Swap Sides'), S.swapIconPos)

    # Update the screen
    pygame.display.flip()


def getImageData(path):
    if path in imageCache.keys():
        return imageCache[path]

    basePath = 'Icons/'
    im = pygame.image.load(basePath + path + '.png')
    imageCache.update({path: im})
    return im

def formatAsTime(seconds):
    hrs, mins, secs = seconds // 3600, (seconds // 60) % 60, seconds % 60

    # Here also could be changed to a 1, if you want:        \|/
    return (f'{hrs:01.0f}:{mins:02.0f}:' if hrs else f'{mins:02.0f}:') + (f'{secs:02.0f}' if mins else f'{secs:06.3f}')