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
        if self.playersPlayed == self.numPlayers:
            self.playersPlayed = 0
            c1 = engine.browseZone('battle', 1)[0]
            c2 = engine.browseZone('battle', 2)[0]
            if( c1.rank > c2.rank ):
                engine.ui.status('Player 1 won the battle')
                engine.unplay(c1,'battle',1)
                engine.unplay(c2,'battle',2)
                tmp = [c1,c2]
                random.shuffle(tmp)
                engine.placeOnBottom(1,'deck', tmp)
                engine.setPhase("next")
            elif( c2.rank > c1.rank ):
                engine.ui.status('Player 2 won the battle')
                engine.unplay(c1,'battle',1)
                engine.unplay(c2,'battle',2)
                tmp = [c1,c2]
                random.shuffle(tmp)
                engine.placeOnBottom(2,'deck', tmp)
                engine.setPhase("next")
            else:
                engine.ui.status('The battle is a draw!')
                engine.setPhase("war")
        else:
            def playCard(e=engine,s=self):
                card = e.draw(e.turn.player)
                e.play(e.draw(e.turn.player),'battle',e.turn.player)
                s.playersPlayed += 1
                e.setTurn(Turn((e.turn.player%s.numPlayers)+1))
            engine.registerOption('play', playCard)

    def war(self,engine):
        engine.ui.status('War!')
        engine.setPhase('next')

    def next(self,engine):
        engine.ui.status('Next!')
        engine.setPhase('play')

    def lose(self,engine):
        engine.ui.status('Player has lost')
        self.ended = True

    def win(self,engine):
        engine.ui.status('Player has won')
        self.ended = True
