from stage import *
from cards import *

class Game:
    '''Classic game of War'''

    def __init__(self,engine,numPlayers):
        engine.registerPhases("setup play war next lose win".split())
        engine.setPhase("setup")
        self.decks = [Deck() for p in range(0,numPlayers)]
        stdDeck().shuffle().deal(self.decks, 27)
        for p in range(1, numPlayers):
            engine.registerZone('battle',p)
            engine.registerZone('war',p)
            engine.registerDeck(self.decks[p],p)
