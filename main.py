from game import Game
from player import Bot, Human
from Bots import RandomBot, BotV1, BotV2

G = Game(BotV1.Bot(doDisplay=True, maxDepth=2), RandomBot.Bot(timePerMove=0.1))
G.run()

# Todo: Make win condition held within game state rather than game, so that win conditions can be evaluated in eval funcs

