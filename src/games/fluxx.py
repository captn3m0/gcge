from cards import * 
from stage import *
import random

class FluxxTurn(Turn):
    def __init__(self, player):
        super().__init__(player)
        self.played = 0
        self.drawn = 0
    def __str__(self):
        return "{0} D{1} P{2}".format(super().__str__(), 
            self.drawn, self.played)

class BasicRules(Card):
    def __init__(self):
        super().__init__("Basic Rules")
        self.priority = 0
    def onplay(self, engine):
        print("Played Basic Rule")
        engine.registerForPhase('play', self)
        engine.registerForPhase('draw', self)
    def onleave(self, engine):
        engine.unregisterForPhase('play', self)
        engine.unregisterForPhase('draw', self)
    def draw(self, engine):
        print("Setting basic limit")
        engine.phase.limit = 1
    def play(self, engine):
        engine.phase.limit = 1
    def isRule(self):
        return True

class DrawN(Card):
    def __init__(self,n):
        super().__init__("Draw {0}".format(n))
        self.n = n
        self.priority = 1
    def onplay(self, engine):
        print("Played {0}".format(self.name))
        engine.registerForPhase('draw', self)
        engine.setPhase('draw')
        for card in engine.browseZone('rules'):
            if card != self and card.name.startswith('Draw '):
                engine.unplay(card, 'rules')
                engine.discard(card)
    def onleave(self, engine):
        print("Discarding {}".format(self.name))
        engine.unregisterForPhase('draw', self)
    def draw(self, engine):
        print("Setting draw limit to {0}".format(self.n))
        engine.phase.limit = self.n
    def isRule(self):
        return True

class PlayN(Card):
    def __init__(self,n):
        super().__init__("Play {0}".format(n))
        self.n = n
        self.priority = 1
    def onplay(self, engine):
        print("Played {0}".format(self.name))
        engine.registerForPhase('play', self)
        engine.setPhase('play')
        for card in engine.browseZone('rules'):
            if card != self and card.name.startswith('Play '):
                engine.unplay(card, 'rules')
                engine.discard(card)
    def onleave(self, engine):
        print("Discarding {}".format(self.name))
        engine.unregisterForPhase('play', self)
    def play(self, engine):
        print("Setting play limit to {0}".format(self.n))
        engine.phase.limit = self.n
    def isRule(self):
        return True

class FirstPlayRandom(Card):
    def __init__(self):
        super().__init__('First Play Random')
        self.priority = 0
    def onplay(self, engine):
        engine.registerForPhase('play', self)
    def play(self, engine):
        player = engine.turn.player
        if engine.turn.played == 0 and engine.hands[player].size() > 0:
            pick = random.randint(0, engine.hands[player].size()-1)
            engine.play(engine.hands[player][pick], 'rules', player, 0)
            engine.turn.played += 1
    def isRule(self):
        return True

# Watch for draw3/play2 - don't count draws and plays against limit

class Fluxx:
    card = {"Basic Rules": BasicRules(), "Draw 2":DrawN(2), "Draw 3":DrawN(3),
                "Play 2":PlayN(2), "Play 3":PlayN(3),
                "FPR":FirstPlayRandom()}

    def info():
        return {'name' : 'Fluxx', 'players' : '2-6'}

    def __init__(self, engine, numPlayers):
        engine.registerPhases("setup draw play done".split())
        engine.setPhase("setup")
        engine.registerZone('rules', 0)
        engine.registerDeck(Fluxx.makeDeck(), 0)
        engine.registerDiscard(Deck(), 0)
        for p in range(1, numPlayers):
            engine.registerZone('keepers', p)
            engine.registerZone('creepers', p)
        self.numPlayers = numPlayers
        engine.ended = False

    def setup(self, engine):
        engine.play(Fluxx.card['Basic Rules'], 'rules')
        # deal 3 cards
        engine.setTurn(FluxxTurn(random.randint(1, self.numPlayers)))
        engine.setPhase("draw")

    def draw(self, engine):
        if engine.turn.drawn < engine.phase.limit:
            def drawCard(e=engine):
                if e.browseZone('deck').size() == 0:
                    e.discardToDraw()
                print('Drew a card')
                e.give(e.turn.player,e.draw(0))
                e.turn.drawn += 1
            engine.registerOption("draw", drawCard)
        else:
            engine.setPhase("play")

    def play(self, engine):
        if engine.turn.played < engine.phase.limit and \
                engine.hands[engine.turn.player].size() > 0:
            engine.registerOption("wait", lambda: 1)
            for card in engine.hands[engine.turn.player]:
                def playCard(e=engine,c=card):
                    if card.isRule:
                        e.play(c, 'rules', e.turn.player, 0)
                    else:
                        e.play(c, 'null', e.turn.player)
                    e.turn.played += 1
                engine.registerOption("play {0}".format(card.name),
                        playCard)
        else:
            engine.setPhase("done")

    def done(self, engine):
        engine.setTurn(FluxxTurn((engine.turn.player%self.numPlayers)+1))
        engine.setPhase("draw")

    def makeDeck():
        deck = Deck([Fluxx.card['FPR'], Fluxx.card['Draw 2'], 
            Fluxx.card['Draw 3'], Fluxx.card['Play 2'], Fluxx.card['Play 3']])
        return deck
