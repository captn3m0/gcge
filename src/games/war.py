from stage import *
from cards import *
import random

class Game:
    '''Classic game of War'''

    def info():
        return {'name' : 'War', 'players' : '2'}

    def __init__(self,engine,numPlayers):
        engine.registerPhases("play war next lose win".split())
        engine.setPhase("play")
        self.decks = [Deck() for p in range(1,numPlayers+1)]
        stdDeck().shuffle().deal(self.decks, 27)
        for p in range(1, numPlayers+1):
            engine.registerZone('battle',p)
            engine.registerZone('war',p)
            print("**",p)
            engine.registerDeck(self.decks[p-1],p)
        self.numPlayers = numPlayers
        engine.setTurn(Turn(1))
        self.playersPlayed=0
        engine.ended = False

    def play(self,engine):
        '''Handle the play phase'''
        def playCard(e=engine):
            e.play(e.draw(e.turn.player),'battle',e.turn.player)
            self.playersPlayed += 1
        playCard()
        engine.setTurn(Turn((engine.turn.player%self.numPlayers)+1))
        if self.playersPlayed == self.numPlayers:
            self.randomPile=[engine.unplay(engine.browseZone('battle',1)[0],'battle',1),engine.unplay(engine.browseZone('battle',2)[0],'battle',2)] 
            if self.randomPile[0].rank > self.randomPile[1].rank:
                random.shuffle(self.randomPile)
                for card in self.randomPile:
                    engine.placeOnBottom(1,'deck',card)
                engine.setPhase("next")
            elif self.randomPile[0].rank < self.randomPile[1].rank:
                random.shuffle(self.randomPile)
                for card in self.randomPile:
                    engine.placeOnBottom(2,'deck',card)
                engine.setPhase("next")
            else:
                engine.setPhase("war") 
    def war(self,engine):
        pass

    def next(self,engine):
        pass

    def lose(self,engine):
        pass

    def win(self,engine):
        pass
