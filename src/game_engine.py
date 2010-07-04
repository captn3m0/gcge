#!/usr/bin/python3

import sys
sys.path.append('./games')
from fluxx import Fluxx

from cards import *
from stage import *

class GameEngine:
    def __init__(self, game, numPlayers):
        self.options = {}
        self.zones = [{} for p in range(-1, numPlayers)]
        self.phaseCallback = {}
        self.hands = dict.fromkeys(range(1,numPlayers+1), [])
        self.game = Fluxx(self, numPlayers)

    def run(self):
        while not self.ended:
            self.options.clear()
            self.procPhase(str(self.phase))
            print("Running phase {0} limit = {1}".format(self.phase,
                  self.phase.limit if hasattr(self.phase,'limit') else 'none'))
            phaseFunc = getattr(self.game, str(self.phase))
            phaseFunc(self)
            if len(self.options):
                choice = input("Choose: " +
                        ",".join(list(self.options.keys())) + "? ")
                if choice in self.options:
                    self.options[choice]()
                else:
                    print("Bad option")

    def registerPhases(self, phases):
        for phase in phases:
            self.phaseCallback[phase] = {}

    def setPhase(self, phase):
        self.phase = Phase(phase)
    def setPlayer(self, player):
        self.player = player
    def setTurn(self, turn):
        self.turn = turn

    def registerDeck(self, deck, player):
        self.zones[player]['deck'] = deck

    def registerDiscard(self, pile, player):
        self.zones[player]['discard'] = pile

    def registerZone(self, zone, player):
        self.zones[player][zone] = []

    def give(self, player, card):
        self.hands[player].append(card)
    def draw(self, zone):
        return self.zones[zone]['deck'].draw()

    def discard(self, player, card):
        self.zones[player]['discard'].append(card)

    def play(self, card, player, controller, zone):
        self.zones[controller][zone].append(card)
        card.onplay(self)
        if player:
            self.hands[player].remove(card)

    def registerOption(self, name, func):
        self.options[name] = func

    def registerForPhase(self, phase, card):
        self.phaseCallback[phase][card] = getattr(card, phase)
    def unregisterForPhase(self, phase, card):
        self.phaseCallback[phase].remove(card)
    def procPhase(self, phase):
        for cbk in sorted(self.phaseCallback[phase].keys(),key=lambda x:x.priority):
            self.phaseCallback[phase][cbk](self)

g = GameEngine('fluxx',2)
g.run()
