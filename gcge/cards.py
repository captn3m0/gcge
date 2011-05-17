import random
import sys

# Check to guarantee python3
if sys.version_info[0] != 3:
    raise SystemError, "Python3 required."

class Card:
    """ TODO -- documentation?

    You might use this class in the following way.

    >>> import gcge.cards
    >>> c = gcge.cards.Card('foo')
    >>> print str(c)
    foo
    >>> c = gcge.cards.Card(name='baz')
    >>> print str(c)
    baz

    """

    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def onplay(self, engine):
        pass
    def onleave(self, engine):
        pass

class Hand:
    """ TODO -- add a docstring here """

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
    def add(self, card):
        self.hand.append(card)
    def remove(self, card):
        self.hand.remove(card)
    def pickRandom(self):
        return self.hand[random.randint(0, self.size()-1)]

class Deck(list):
    def __init__(self, cards=None):
        if cards != None:
            self.extend(cards)
    def __str__(self):
        return "[{}]".format(":".join(map(str,self)))

    def size(self):
        return len(self)

    def add(self, card):
        self.append(card)

    def shuffleIn(self, cards):
        self.extend(cards)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self)
        return self

    def deal(self, dest, num):
        for i in range(0, num):
            for d in dest:
                card = self.draw()
                d.add(card)

    def draw(self):
        return self.pop(0)

class PlayingCard(Card):
    """ A specialization of :class:`Card` that represents a playing card
    in a typical Western card deck.

    >>> import gcge.cards
    >>> c = gcge.cards.PlayingCard('H', '2', 'what-is-rank')
    >>> print str(c)
    Two of Hearts

    """

    suit = {"H":"Heart","C":"Club","D":"Diamond","S":"Spade","N":"None"}
    value = {"2":"Two","3":"Three","4":"Four","5":"Five","6":"Six",
              "7":"Seven","8":"Eight","9":"Nine","0":"Ten",
              "J":"Jack","Q":"Queen","K":"King","A":"Ace","O":"Joker"}
    def __init__(self, suit,value,rank):
        if value == "O":
            name = PlayingCard.value[value]
        else :
            name = PlayingCard.value[value] + " of " + \
                    PlayingCard.suit[suit] + "s"
        super().__init__(name)
        self.suit = suit
        self.value = value
        self.rank = rank
    def __str__(self):
        return self.name

def makePlayingCardDeck(ranking,suits):
    rank = 0
    cards = []
    for value in list(ranking):
        if value == " ":
            rank += 1
        elif value == "O":
            card = PlayingCard("N",value,rank)
            cards.append(card)
            card = PlayingCard("N",value,rank)
            cards.append(card)
        else:
            for suit in list(suits):
                card = PlayingCard(suit,value,rank)
                cards.append(card)
    deck = Deck(cards)
    return deck

def stdDeck():
    return makePlayingCardDeck("O 2 3 4 5 6 7 8 9 0 J Q K A","HDCS")
