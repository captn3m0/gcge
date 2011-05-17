from cards import *

import copy

class FluxxCard(Card):
    def __init__(self, name, type, priority = 0):
        Card.__init__(self, name)
        self.priority = priority
        self.type = type
    def playself(self, engine, to=None, _from=None):
        if to == None:
            to = engine.turn.player
        if _from == None:
            _from = engine.hands[to]
        if self.type == 'rule':
            engine.play(self, 'rules', hand=_from)
        elif self.type == 'keeper':
            engine.play(self, 'keepers', to, _from)
        elif self.type == 'creeper':
            engine.play(self, 'creepers', to, _from)
        elif self.type == 'action':
            engine.play(self, 'actions', to, _from)

class BasicRules(FluxxCard):
    def __init__(self):
        FluxxCard.__init__(self, "Basic Rules", 'rule')
    def onplay(self, engine):
        engine.ui.status("Played Basic Rule")
        engine.registerForPhase('play', self)
        engine.registerForPhase('draw', self)
    def onleave(self, engine):
        engine.unregisterForPhase('play', self)
        engine.unregisterForPhase('draw', self)
    def draw(self, engine):
        engine.phase.limit = 1
    def play(self, engine):
        engine.phase.limit = 1

class DrawN(FluxxCard):
    def __init__(self,n):
        FluxxCard.__init__(self, "Draw {0}".format(n), 'rule', 1)
        self.n = n
    def onplay(self, engine):
        engine.ui.status("Played {0}".format(self.name))
        engine.registerForPhase('draw', self)
        engine.setPhase('draw')
        for card in engine.browseZone('rules'):
            if card != self and card.name.startswith('Draw '):
                engine.unplay(card, 'rules')
                engine.discard(card)
    def onleave(self, engine):
        engine.ui.status("Discarding {}".format(self.name))
        engine.unregisterForPhase('draw', self)
    def draw(self, engine):
        engine.phase.limit = self.n

class PlayN(FluxxCard):
    def __init__(self,n):
        FluxxCard.__init__(self, "Play {0}".format(n), 'rule', 1)
        self.n = n
    def onplay(self, engine):
        engine.ui.status("Played {0}".format(self.name))
        engine.registerForPhase('play', self)
        engine.setPhase('play')
        for card in engine.browseZone('rules'):
            if card != self and card.name.startswith('Play '):
                engine.unplay(card, 'rules')
                engine.discard(card)
    def onleave(self, engine):
        engine.ui.status("Discarding {}".format(self.name))
        engine.unregisterForPhase('play', self)
    def play(self, engine):
        engine.phase.limit = self.n

class FirstPlayRandom(FluxxCard):
    def __init__(self):
        FluxxCard.__init__(self, 'First Play Random', 'rule')
    def onplay(self, engine):
        engine.registerForPhase('play', self)
    def play(self, engine):
        player = engine.turn.player
        if engine.turn.played == 0 and engine.hands[player].size() > 0:
            engine.hands[player].pickRandom().playself(engine, player)
            engine.turn.played += 1

class DrawNPlayM(FluxxCard):
    def __init__(self, draw, play):
        FluxxCard.__init__(self, 'Draw {}, Play {}'.format(draw,play), 'action')
        self.draw = draw
        self.play = play
    def onplay(self, engine):
        engine.registerForPhase('action', self)
        engine.setPhase('action')
        self.drawn = 0
        self.played = 0
        self.temphand = []
    def onleave(self, engine):
        engine.unregisterForPhase('action', self)
    def action(self, engine):
        engine.ui.status("In {} Drawn{}/{} Played {}/{}".format(self.name,
            self.drawn, self.draw, self.played, self.play))
        player = engine.turn.player
        if self.drawn < self.draw:
            def drawCard(e=engine, s=self):
                if e.browseZone('deck').size() == 0:
                    e.discardToDraw()
                s.temphand.append(e.draw(0))
                s.drawn += 1
            engine.registerOption("draw", drawCard)
            engine.setPhase("action")
        elif self.played < self.play:
            for card in self.temphand:
                def playCard(e=engine, s=self, c=card):
                    c.playself(e, player, _from=s.temphand)
                    s.played += 1
                engine.registerOption("play {}".format(card.name), playCard)
            engine.setPhase("action")
        else:
            for card in self.temphand:
                engine.discard(card)
            engine.discard(engine.unplay(self, 'actions', player))
            engine.setPhase("draw")

class Keeper(FluxxCard):
    def __init__(self, name, _type=None):
        FluxxCard.__init__(self, name, 'keeper')
        if _type == None:
            self.classification = name
        else:
            self.classification = _type
