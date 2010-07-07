from cards import * 

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

