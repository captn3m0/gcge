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

class PlayingCard(Card):
    suit = {"H":"Heart","C":"Club","D":"Diamond","S":"Spade","N":"None"}
    value = {"2":"Two","3":"Three","4":"Four","5":"Five","6":"Six",
              "7":"Seven","8":"Eight","9":"Nine","0":"Ten",
              "J":"Jack","Q":"Queen","K":"King","A":"Ace","O":"Joker"}
    def __init__(self, name,suit,value,rank):
        super().__init__(name)
        self.name = name
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
            name = PlayingCard.value[value]
            card = PlayingCard(name,"N",value,rank) 
            cards.append(card)
            print(card,"added")
            card = PlayingCard(name,"N",value,rank) 
            cards.append(card)
            print(card,"added")
        else:
            for suit in list(suits):
                name = PlayingCard.value[value] + " of " + PlayingCard.suit[suit] + "s"
                card = PlayingCard(name,suit,value,rank) 
                cards.append(card)
                print(card,"added")
    deck = Deck(cards) 
    return deck

def stdDeck():
    return makePlayingCardDeck("O 2 3 4 5 6 7 8 9 0 J Q K A","HDCS")
