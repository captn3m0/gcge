class Player:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.hand = []

    def giveCard(self,card):
        self.hand.append(card)

    def takeCard(self,card):
        self.hand.remove(card)
