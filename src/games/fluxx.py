#!/usr/bin/python3

from Deck import Deck
import random

class FluxxTurn(Turn):
    def __init__(self,player):
        super().__init__(player)
        self.played = 0
        self.drawn = 0

class Fluxx:
    card = {"Basic Rules":"draw 1 play 1"}

    def info():
        return {'name' : 'Fluxx', 'players' : '2-6'}

    def __init__(self, engine, numPlayers):
        self.phases = "setup draw play done".split()
        self.phase = Phase("setup")
        self.playField = []
        self.deck = Fluxx.makeDeck()
        self.discard = []
        for p in range(1, numPlayers):
            engine.registerDeck(self.deck, p)
            engine.registerDiscard(self.discard, p)
        self.numPlayers = numPlayers
        self.ended = False

    def setup(self,engine):
        self.engine.play(Fluxx.card['Basic Rules'],'rules')
        self.deck.deal(self.numPlayers, 3)
        self.player = random.randint(1,self.numPlayers)
        self.turn = FluxxTurn(self.player)
        self.phase = "draw"

    def draw(self,engine):
        engine.registerOption("draw", self.drawCard)
        if self.turn.limit == self.turn.drawn:
            self.phase = "play"

    def drawCard(self):
        #self.drawn
        print("Drew a card")

    def play(self,engine):
        if self.turn.played < self.turn.limit:
            #for card in self.
            pass

    def done(self,engine):
        pass

    def makeDeck():
        return Deck()
            #if phase == "draw":
                #limit = 1
            #if phase == "play":
                #limit = 1
        
