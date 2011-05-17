from cards import Deck

class Game:
    '''All game rule classes must be named "Game"'''

    def info():
        return {'name':'Example Skeleton Rules', 'players':'0'}

    def __init__(self, engine, numPlayers):
        '''init should: register phases, choose the initial phase,
                register any decks/discards/other zones,
                and set ended to False'''
        engine.registerPhases("setup lose".split())
        engine.setPhase('setup')
        engine.registerDeck(Deck(), 0)
        engine.ended = False

    def setup(self, engine):
        '''Game must define a function for each registered phase'''
        engine.setPhase('lose')

    def lose(self, engine):
        engine.ui.status("You lost!")
        engine.ended = True
        
