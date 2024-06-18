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

        self.highlightedTiles = []

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

        self.font = pygame.font.Font(fontPath, self.timeTextSize)
        self.padding = self.timeTextSize // 3

    def sideColor(self, s):
        """Returns the correct tile color for a specific side."""
        if Side('w') == s:
            return self.lightColor
        if Side('b') == s:
            return self.darkColor

    def textBackgroundColor(self, player, side):
        """Returns either active or inactive background color."""
        return self.timeTextActiveBackgroundColor if side != player.game.G.turn else self.timeTextInactiveBackgroundColor


def drawBoard(b, D, clickedCondition=lambda x: False, highlightCondition=lambda x: False, flip=True):
    window = D.displaySurface
    window.fill(0)

    for i in range(64):
        coords = np.array((i % 8, i // 8))  # Tile coordinates on board
        if D.displaySide == 'b':
            coords = 7 - coords

        tilePos = (D.tileSize * coords) + D.borderSize  # Tile position on display

        # Draw Tile
        tileColor = [D.sideColor(1 - (coords.sum() % 2))]
        if clickedCondition(i):
            tileColor.append(D.clickedColor)  # Repeated to get a 2:1 weighted average
            tileColor.append(D.clickedColor)
        if highlightCondition(i):
            tileColor.append(D.highlightColor)  # Repeated to get a 2:1 weighted average
            tileColor.append(D.highlightColor)

        gammaFactor = 0.1
        tileColor = np.clip(((np.mean(np.array(tileColor) ** gammaFactor, axis=0)) ** (1 / gammaFactor)), 0, 255)  # Gamma-correcting color average

        pygame.draw.rect(window, tileColor, pygame.Rect(*tilePos, D.tileSize, D.tileSize))

        # Draw Peice
        if (peice := b[i]) != ' ':
            path = ('1' if peice.isupper() else '0') + str(peice).lower()
            window.blit(getImageData(path), tilePos)

    if flip:
        pygame.display.flip()


def drawTimeText(player, flip=False):
    D = player.displaySettings
    window = D.displaySurface

    for side in (player.s, -player.s):
        timeText = D.font.render(formatAsTime(player.game.timeRemaining[side.i]), True, D.timeTextColor)
        rs = np.array(timeText.get_size())
        if side == player.s:
            textPos = np.array((D.borderSize[0] - rs[0] - 2 * D.padding,
                                D.windowSize[1] - D.borderSize[1] - D.timeTextSize - D.padding))
        else:
            textPos = np.array(
                (D.borderSize[0] - rs[0] - 2 * D.padding, D.borderSize[1] + D.timeTextSize - rs[1] + D.padding))
        backgroundRect = pygame.rect.Rect(*(textPos - D.padding), *(rs + 2 * D.padding))
        pygame.draw.rect(window, D.textBackgroundColor(player, side), backgroundRect)
        window.blit(timeText, textPos)

    if flip:
        pygame.display.flip()


def draw(player):
    S = player.displaySettings
    window = S.displaySurface
    b = player.game.G.board if S.displayMoveHistory is None else player.game.G.boardHistory[S.displayMoveHistory]

    # Display Board
    drawBoard(b, S, lambda x: hasattr(player, 'selected') and x == player.selected, lambda x: x in S.highlightedTiles, False)

    # Display Time Text
    drawTimeText(player)

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