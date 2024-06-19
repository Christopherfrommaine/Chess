from game import Game
from player import Bot, Human
from Bots.BotV1 import BotV1

G = Game(Human(), BotV1())
# G = Game(Human(), Bot())
G.run()

