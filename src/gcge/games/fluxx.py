from stage import *
from fluxx_cards import *
import random

class FluxxTurn(Turn):
    '''A player's turn recording number of cards drawn and played that turn'''
    def __init__(self, player):
        Turn.__init__(self,player)
        self.drawn = 0
        self.played = 0
    def __str__(self):
        return "{0} D{1} P{2}".format(Turn.__str__(self), 
            self.drawn, self.played)

# Watch for draw3/play2 - don't count draws and plays against limit

class Game:
    '''The Fluxx card game
    
    Produced by Looney Labs - http://looneylabs.com
    Buy the real thing!'''

    card = {"Basic Rules": BasicRules(), "Draw 2":DrawN(2), "Draw 3":DrawN(3),
                "Play 2":PlayN(2), "Play 3":PlayN(3),
                "FPR":FirstPlayRandom(), "D3P2":DrawNPlayM(3,2),
                "D2P2":DrawNPlayM(2,2)}
    keeper = (  Keeper('The Shovel','pow'), Keeper('Lumber','pow'),
                Keeper('The Car', 'pow'), Keeper('Can of Gasoline', 'pow'),
                Keeper('Donuts'), Keeper('The Chainsaw', 'pow'), 
                Keeper('Coffee'), Keeper('Baseball Bat', 'pow'), 
                Keeper('Sandwiches'), Keeper('Brains'),
                Keeper('A Friend', 'friend')
                )

    def info():
        return {'name' : 'Fluxx', 'players' : '2-6'}

    def __init__(self, engine, numPlayers):
        engine.registerPhases("setup action draw play done".split())
        engine.setPhase("setup")
        engine.registerZone('rules', 0)
        engine.registerDeck(Game.makeDeck(), 0)
        engine.registerDiscard(Deck(), 0)
        for p in range(1, numPlayers+1):
            engine.registerZone('keepers', p)
            engine.registerZone('creepers', p)
            engine.registerZone('actions', p)
        self.numPlayers = numPlayers
        engine.ended = False

    def setup(self, engine):
        engine.play(Game.card['Basic Rules'], 'rules')
        # deal 3 cards
        engine.setTurn(FluxxTurn(random.randint(1, self.numPlayers)))
        engine.setPhase("draw")

    def draw(self, engine):
        '''Handle the draw phase'''
        if engine.turn.drawn < engine.phase.limit:
            def drawCard(e=engine):
                if e.browseZone('deck').size() == 0:
                    e.discardToDraw()
                e.give(e.turn.player,e.draw(0))
                e.turn.drawn += 1
            engine.registerOption("draw", drawCard)
        else:
            engine.setPhase("play")

    def play(self, engine):
        '''Handle the play phase'''
        if engine.turn.played < engine.phase.limit and \
                engine.hands[engine.turn.player].size() > 0:
            engine.registerOption("wait", lambda: 1)
            for card in engine.hands[engine.turn.player]:
                def playCard(e=engine,c=card):
                    c.playself(e, e.turn.player)
                    e.turn.played += 1
                engine.registerOption("play {0}".format(card.name),
                        playCard)
        else:
            engine.setPhase("done")

    def action(self, engine):
        '''Actions mostly handle themselves'''
        pass

    def done(self, engine):
        '''Handle the end of the turn'''
        engine.setTurn(FluxxTurn((engine.turn.player%self.numPlayers)+1))
        engine.setPhase("draw")

    def makeDeck():
        '''Return a Deck() containing the cards for this game'''
        deck = Deck([Game.card['FPR'], Game.card['D3P2'], Game.card['Draw 2'], 
            Game.card['Draw 3'], Game.card['Play 2'], Game.card['Play 3'],
            Game.card['D2P2']])
        deck.shuffleIn(Game.keeper)
        deck.shuffle()
        return deck
