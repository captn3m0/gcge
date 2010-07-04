import random

class Card:
    def play(self,engine):
        pass

class Deck:
    def __init__(self):
        self.cards = []

    def shuffle(self):
        random.shuffle(cards)

    def deal(self, who, num):
        pass

    def draw(self):
        return self.cards.pop(0)
