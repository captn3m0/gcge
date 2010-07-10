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
    def __getitem__(self, index):
        return self.hand[index]

    def size(self):
        return len(self.hand)
    def give(self, card):
        self.hand.append(card)
    def remove(self, card):
        self.hand.remove(card)
    def pickRandom(self):
        return self.hand[random.randint(0, self.size()-1)]

class Deck:
    def __init__(self, cards=[]):
        self.cards = cards
    def __iter__(self):
        return self.cards.__iter__()
    def __getitem__(self, index):
        return self.cards[index]

    def size(self):
        return len(self.cards)

    def add(self, card):
        self.cards.append(card)

    def shuffleIn(self, cards):
        self.cards.extend(cards)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, who, num):
        pass

    def draw(self):
        return self.cards.pop(0)
