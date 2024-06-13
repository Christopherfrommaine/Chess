import time

from game import Game
from player import Bot, Human

# G = Game(Human(), Bot())
G = Game(Bot(), Human())
G.run()

time.sleep(20)

G.Pb.stopDisplay()
