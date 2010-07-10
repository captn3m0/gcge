from stage import *
from cards import *

class Game:
    '''Classic game of War'''

    def info():
        return {'name' : 'War', 'players' : '2'}

    def __init__(self,engine,numPlayers):
        engine.registerPhases("play war next lose win".split())
        engine.setPhase("play")
        self.decks = [Deck() for p in range(0,numPlayers+1)]
        stdDeck().shuffle().deal(self.decks, 27)
        for p in range(1, numPlayers+1):
            engine.registerZone('battle',p)
            engine.registerZone('war',p)
            engine.registerDeck(self.decks[p],p)
        self.numPlayers = numPlayers
        engine.ended = False

    def play(self,engine):
        '''Handle the play phase'''
        def playCard(e=engine):

    def war(self,engine):

    def next(self,engine):

    def lose(self,engine):

    def win(self,engine):
