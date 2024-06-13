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
    def __init__(self, windowSize=(1280, 720), tileSize=60, timeTextSize=24, lightColor=(191, 131, 80), darkColor=(128, 78, 37), highlightColor=(200, 200, 0), clickedColor=(200, 100, 100), timeTextColor=(255, 255, 255), timeTextActiveBackgroundColor=(50, 50, 50), timeTextInactiveBackgroundColor=(100, 100, 100)):
        self.displaySurface = None
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
        if Side('w') == s:
            return self.lightColor
        if Side('G') == s:
            return self.darkColor

    def textBackgroundColor(self, player, op=None):
        if op is None:
            return self.timeTextActiveBackgroundColor if player.s != player.game.G.turn else self.timeTextInactiveBackgroundColor
        return self.timeTextActiveBackgroundColor if player.s == player.game.G.turn else self.timeTextInactiveBackgroundColor


def draw(player):
    S = player.displaySettings
    window = S.displaySurface
    side = S.displaySide

    # S.displaySide = Side('w')

    window.fill(0)

    for i in range(64):
        # time.sleep(1)
        # pygame.display.flip()
        coords = np.array((i % 8, i // 8))  # Tile coords on board
        if side == 'b':
            coords = 7 - coords

        tilePos = (S.tileSize * coords) + S.borderSize  # Tile position on display

        # Draw Tile
        tileColor = S.sideColor(1 - (coords.sum() % 2))
        if hasattr(player, 'selected'):
            if i == player.selected:
                tileColor = 0.2 * np.array(tileColor) + 0.8 * np.array(S.clickedColor)
        pygame.draw.rect(window,
                         tileColor,
                         pygame.Rect(*tilePos, S.tileSize, S.tileSize))

        # Draw Peice
        if (peice := player.game.G.board[i]) != ' ':
            path = ('1' if peice.isupper() else '0') + str(peice).lower()
            window.blit(getImageData(path), tilePos)

    # Get Time Text Font
    font = pygame.font.Font(fontPath, S.timeTextSize)
    padding = S.timeTextSize // 3

    # Display Player Time Text:
    timeText = font.render(formatAsTime(player.game.timeRemaining[player.s.i]), True, S.timeTextColor)
    rs = np.array(timeText.get_size())
    textPos = np.array((S.borderSize[0] - rs[0] - 2 * padding, S.windowSize[1] - S.borderSize[1] - S.timeTextSize - padding))
    backgroundRect = pygame.rect.Rect(*(textPos - padding), *(rs + 2 * padding))
    pygame.draw.rect(window, S.textBackgroundColor(player), backgroundRect)
    window.blit(timeText, textPos)

    # Display Opponent Time Text:
    timeText = font.render(formatAsTime(player.game.timeRemaining[1 - player.s.i]), True, S.timeTextColor)
    textPos = (S.borderSize[0] - timeText.get_size()[0] - 2 * padding, S.borderSize[1] + S.timeTextSize - timeText.get_size()[1] + padding)
    backgroundRect = pygame.rect.Rect(textPos[0] - padding, textPos[1] - padding, timeText.get_size()[0] + 2 * padding, timeText.get_size()[1] + 2 * padding)
    pygame.draw.rect(window, S.textBackgroundColor(player, 'opponent'), backgroundRect)
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