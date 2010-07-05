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
        self.hands = {}
        for p in range(1,numPlayers+1):
            self.hands[p] = Hand(p)
        self.game = Fluxx(self, numPlayers)

    def run(self):
        while not self.ended:
            self.options.clear()
            if len(self.nextphase):
                self.phase = self.nextphase.pop(0)
            phase = self.phase
            self.procPhase(phase)
            try:
                print(" ".join(map(str,[self.turn, phase,
                        self.hands[self.turn.player]])))
            except AttributeError as a:
                print(a)
            phaseFunc = getattr(self.game, phase.name)
            phaseFunc(self)
            if len(self.options):
                self.registerOption('exit', sys.exit)
                choice = input("Choose: " +
                        ",".join(list(self.options.keys())) + "? ")
                if choice in self.options:
                    self.options[choice]()
                else:
                    print("Bad option")

    def registerPhases(self, phases):
        self.nextphase = []
        self.phaseOrder = {}
        index = 0
        for phase in phases:
            self.phaseOrder[phase] = index
            index += 1
            self.phaseCallback[phase] = {}

    def setPhase(self, phase):
        self.nextphase.append(Phase(phase))
        self.nextphase.sort(key=lambda p:self.phaseOrder[p.name])
    def setTurn(self, turn):
        self.turn = turn

    def registerDeck(self, deck, player):
        self.zones[player]['deck'] = deck

    def registerDiscard(self, pile, player):
        self.zones[player]['discard'] = pile

    def registerZone(self, zone, player):
        self.zones[player][zone] = []

    def give(self, player, card):
        print("Giving player {0} card {1}".format(player,card))
        self.hands[player].give(card)
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
        for cbk in sorted(self.phaseCallback[phase.name].keys(),
                key=lambda c:c.priority):
            self.phaseCallback[phase.name][cbk](self)

g = GameEngine('fluxx',2)
g.run()
