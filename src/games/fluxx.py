from cards import * 
from stage import *
import random

class FluxxTurn(Turn):
    def __init__(self, player):
        super().__init__(player)
        self.played = 0
        self.drawn = 0
        print("Player {0}'s turn".format(player))

class BasicRules(Card):
    def __init__(self):
        self.name = "Basic Rules"
        self.priority = 0
    def onplay(self, engine):
        print("Played Basic Rule")
        engine.registerForPhase('play', self)
        engine.registerForPhase('draw', self)
    def onleave(self, engine):
        engine.unregister(self)
    def draw(self, engine):
        print("Setting basic limit")
        engine.phase.limit = 1
    def play(self, engine):
        engine.phase.limit = 1
    def isRule(self):
        return True

class DrawN(Card):
    def __init__(self,n):
        self.n = n
        self.name = "Draw {0}".format(n)
        self.priority = 1
    def onplay(self, engine):
        print("Played {0}".format(self.name))
        engine.registerForPhase('draw', self)
        engine.setPhase('draw')
    def draw(self, engine):
        print("Setting card limit to {0}".format(self.n))
        engine.phase.limit = self.n
    def isRule(self):
        return True

# Watch for draw3/play2 - don't count draws and plays against limit

class Fluxx:
    card = {"Basic Rules": BasicRules(), "Draw 2":DrawN(2), "Draw 3":DrawN(3)}

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
        engine.play(Fluxx.card['Basic Rules'], 0, 0, 'rules')
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
        if engine.turn.played < engine.phase.limit:
            engine.registerOption("wait", lambda: x)
            for card in engine.hands[engine.player]:
                def playCard(e=engine):
                    if card.isRule:
                        e.play(card,e.player,0,'rules')
                    else:
                        e.play(card,e.player,e.player,'null')
                    e.turn.played += 1
                engine.registerOption("play {0}".format(card.name),
                        playCard)
        else:
            engine.setPhase("done")

    def done(self, engine):
        engine.setPlayer((engine.player%self.numPlayers)+1)
        engine.setTurn(FluxxTurn(engine.player))
        engine.setPhase("draw")

    def makeDeck():
        deck = Deck([Fluxx.card['Draw 2'], Fluxx.card['Draw 3'],
            Fluxx.card['Draw 2'], Fluxx.card['Draw 3']])
        return deck
