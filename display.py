import pygame
import numpy as np
from side import Side

pygame.init()

class DisplaySettings:
    def __init__(self, windowSize=(1280, 720), tileSize=60, timeTextSize=24, lightColor=(191, 131, 80), darkColor=(128, 78, 37), highlightColor=(200, 200, 0), clickedColor=(200, 100, 100), timeTextColor=(200, 200, 200)):
        self.displaySurface = None
        self.displaySide = None
        self.displayThread = None

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

    def sideColor(self, s):
        if Side('w') == s:
            return self.lightColor
        if Side('G') == s:
            return self.darkColor


def draw(player):
    S = player.displaySettings
    window = S.displaySurface

    window.fill(0)

    for i in range(64):
        coords = np.array((i % 8, i // 8))  # Tile coords on board
        if S.displaySide == 'G':
            coords = 7 - coords

        tilePos = (S.tileSize * coords) + S.borderSize  # Tile position on display

        # Draw Tile
        tileColor = S.sideColor(1 - (coords.sum() % 2))
        # TODO: add highlight and clicked color logic here, once implemented
        pygame.draw.rect(window,
                         tileColor,
                         pygame.Rect(*tilePos, S.tileSize, S.tileSize))

        # Draw Peice
        if (peice := player.game.G.board[i]) != ' ':
            path = ('1' if peice.isupper() else '0') + str(peice).lower()
            window.blit(getImageData(path), tilePos)

    # Get Time Text Font
    try:
        fontPath = pygame.font.match_font('microsoftsansserif')
    except Exception:
        fontPath = pygame.font.get_default_font()
    font = pygame.font.Font(fontPath, S.timeTextSize)
    padding = S.timeTextSize // 4

    # Display Player Time Text:
    timeText = font.render(formatAsTime(player.game.timeRemaining[player.s.i]), True, S.timeTextColor)
    textPos = (S.borderSize[0] - timeText.get_size()[0] - 2 * padding, S.windowSize[1] - S.borderSize[1] - S.timeTextSize)
    window.blit(timeText, textPos)

    # Display Opponent Time Text:
    timeText = font.render(formatAsTime(player.game.timeRemaining[1 - player.s.i]), True, S.timeTextColor)
    textPos = (S.borderSize[0] - timeText.get_size()[0] - 2 * padding, S.borderSize[1] + S.timeTextSize - timeText.get_size()[1])
    window.blit(timeText, textPos)

    # Display Swap Icon
    window.blit(getImageData('Swap Sides'), S.swapIconPos)

    # Update the screen
    pygame.display.flip()


def getImageData(path):
    # TODO: a potential optimization would be to cache the images
    basePath = 'Icons/'
    return pygame.image.load(basePath + path + '.png')

def formatAsTime(seconds):
    hrs, mins, secs = seconds // 3600, (seconds // 60) % 60, seconds % 60

    # Here also could be changed to a 1, if you want:        \|/
    return (f'{hrs:01.0f}:{mins:02.0f}:' if hrs else f'{mins:02.0f}:') + (f'{secs:02.0f}' if mins else f'{secs:06.3f}')

