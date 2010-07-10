#!/usr/bin/python3

import sys
sys.path.append('./games')
sys.path.append('./ui')

from cards import Hand
from stage import Phase

class GameEngine:
    def __init__(self, game, numPlayers, ui='text'):
        uiMod = __import__('ui.'+ui, fromlist='ui')
        self.options = {}
        self.zones = [{} for p in range(-1, numPlayers)]
        self.phaseCallback = {}
        self.hands = {}
        for p in range(1,numPlayers+1):
            self.hands[p] = Hand(p)
        gameMod = __import__(game)
        self.game = gameMod.Game(self, numPlayers)
        self.ui = uiMod.UI(self, numPlayers)
        self.ui.start()

    def run(self):
        while not self.ended:
            self.step()

    def step(self):
            self.options.clear()
            if len(self.nextphase):
                self.phase = self.nextphase.pop(0)
            phase = self.phase
            self.procPhase(phase)
            try:
                self.ui.status(" ".join(map(str,[self.turn, phase,
                        self.hands[self.turn.player]])))
            except AttributeError as a:
                #self.ui.status(a)
                pass
            phaseFunc = getattr(self.game, phase.name)
            phaseFunc(self)
            if len(self.options):
                self.registerOption('exit', sys.exit)
                self.ui.prompt(self.options)

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
        self.ui.status("Giving player {0} card {1}".format(player,card))
        self.hands[player].add(card)
    def draw(self, zone):
        return self.zones[zone]['deck'].draw()

    def discard(self, player, card):
        self.zones[player]['discard'].append(card)

    def discardToDraw(self, discard=0, deck=0):
        self.ui.status("Shuffling discard to deck")
        self.zones[deck]['deck'].shuffleIn(self.zones[discard]['discard'])
        self.zones[discard]['discard'] = []

    def browseZone(self, zone, controller=0):
        return self.zones[controller][zone]

    def play(self, card, zone, controller=0, hand=None):
        self.zones[controller][zone].append(card)
        card.onplay(self)
        if hand:
            hand.remove(card)
    def unplay(self, card, zone, controller=0):
        self.zones[controller][zone].remove(card)
        card.onleave(self)
        return card
    def discard(self, card, controller=0, zone='discard', hand=None):
        self.zones[controller][zone].add(card)
        if hand:
            hand.remove(card)

    def registerOption(self, name, func):
        self.options[name] = func

    def registerForPhase(self, phase, card):
        self.phaseCallback[phase][card] = getattr(card, phase)
    def unregisterForPhase(self, phase, card):
        self.phaseCallback[phase].pop(card, None)
    def procPhase(self, phase):
        for cbk in sorted(self.phaseCallback[phase.name].keys(),
                key=lambda c:c.priority):
            self.phaseCallback[phase.name][cbk](self)

if __name__ == '__main__':
    game = 'fluxx'
    players = 2
    ui = 'text'
    if len(sys.argv) > 1:
        game = sys.argv[1]
    if len(sys.argv) > 2:
        players = int(sys.argv[2])
    if len(sys.argv) > 3:
        ui = sys.argv[3]
    g = GameEngine(game, players, ui)
