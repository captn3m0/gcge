from cards import * 
from stage import *
import random

class FluxxTurn(Turn):
    def __init__(self, player):
        super().__init__(player)
        self.played = 0
        self.drawn = 0

class BasicRules(Card):
    def onplay(self, engine):
        engine.registerForPhase('play', self)
        engine.registerForPhase('draw', self)
    def onleave(self, engine):
        engine.unregister(self)
    def draw(self, engine):
        engine.phase.limit = 1
    def play(self, engine):
        engine.phase.limit = 1

# Watch for draw3/play2 - don't count draws and plays against limit

class Fluxx:
    card = {"Basic Rules": BasicRules()}

    def info():
        return {'name' : 'Fluxx', 'players' : '2-6'}

    def __init__(self, engine, numPlayers):
        engine.registerPhases("setup draw play done".split())
        engine.setPhase("setup")
        engine.registerZone('rules', 0)
        engine.registerDeck(Fluxx.makeDeck(), 0)
        engine.registerDiscard([], 0)
        for p in range(1, numPlayers):
            engine.registerZone('keepers', p)
            engine.registerZone('creepers', p)
        self.numPlayers = numPlayers
        engine.ended = False

    def setup(self, engine):
        engine.play(Fluxx.card['Basic Rules'], 0, 'rules')
        # deal 3 cards
        engine.setPlayer(random.randint(1, self.numPlayers))
        engine.setTurn(FluxxTurn(engine.player))
        engine.setPhase("draw")

    def draw(self, engine):
        if engine.turn.drawn < engine.phase.limit:
            def drawCard(e=engine):
                print('Drew a card')
                e.give(e.player,e.draw(0))
                e.turn.drawn += 1
            engine.registerOption("draw", drawCard)
        else:
            engine.setPhase("play")

    def play(self, engine):
        if engine.turn.played < self.phase.limit:
            #for card in self.
            engine.registerOption("play", self.drawCard)
        else:
            engine.setPhase("done")

    def done(self, engine):
        pass

    def makeDeck():
        return Deck()
