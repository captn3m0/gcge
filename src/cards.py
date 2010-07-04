import random

class Card:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Hand:
    def __init__(self, player):
        self.player = player
        self.hand = []
    def __str__(self):
        return "Hand [{0}]".format(":".join(map(str, self.hand)))
    def __iter__(self):
        return self.hand.__iter__()

    def size(self):
        return len(self.hand)
    def give(self, card):
        self.hand.append(card)
    def remove(self, card):
        self.hand.remove(card)

class Deck:
    def __init__(self):
        self.cards = []

    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        random.shuffle(cards)

    def deal(self, who, num):
        pass

    def draw(self):
        return self.cards.pop(0)
