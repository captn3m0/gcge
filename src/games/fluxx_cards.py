from cards import * 

class FluxxCard(Card):
    def __init__(self, name, type, priority = 0):
        super().__init__(name)
        self.priority = priority
        self.type = type
    def playself(self, engine, player):
        if self.type == 'rule':
            engine.play(self, 'rules', player, 0)
        elif self.type == 'keeper':
            engine.play(self, 'keepers', player)
        elif self.type == 'creeper':
            engine.play(self, 'creepers', player)
        elif self.type == 'action':
            engine.play(self, 'actions', player)

class BasicRules(FluxxCard):
    def __init__(self):
        super().__init__("Basic Rules", 'rule')
    def onplay(self, engine):
        print("Played Basic Rule")
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
        super().__init__("Draw {0}".format(n), 'rule', 1)
        self.n = n
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
        #print("Setting draw limit to {0}".format(self.n))
        engine.phase.limit = self.n

class PlayN(FluxxCard):
    def __init__(self,n):
        super().__init__("Play {0}".format(n), 'rule', 1)
        self.n = n
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
        #print("Setting play limit to {0}".format(self.n))
        engine.phase.limit = self.n

class FirstPlayRandom(FluxxCard):
    def __init__(self):
        super().__init__('First Play Random', 'rule')
    def onplay(self, engine):
        engine.registerForPhase('play', self)
    def play(self, engine):
        player = engine.turn.player
        if engine.turn.played == 0 and engine.hands[player].size() > 0:
            engine.hands[player].pickRandom().playself(engine, player)
            engine.turn.played += 1

