#!/usr/bin/python3

from fluxx import Fluxx

class GameEngine:
    def __init__(self):
        self.game = Fluxx(self, 2)
        self.options = {}

    def run(self):
        while not self.game.ended:
            self.options.clear()
            phase = getattr(self.game, str(self.game.phase))
            phase(self)
            if self.options:
                choice = input("Choose: " +
                        ",".join(list(self.options.keys())) + "? ")
                if choice in self.options:
                    self.options[choice]()
                else:
                    print("Bad option")

    def registerDeck(self,deck,player):
        pass

    def registerDiscard(self,pile,player):
        pass

    def registerZone(self,zone,player):
        self.zones[player][zone] = []

    def play(self,card,player,zone):
        self.zones[player][zone].append(card)
        card.play(self)

    def registerOption(self,name,func):
        self.options[name] = func


g = GameEngine()
g.run()
