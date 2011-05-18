class Player:
    """ Represents a player in the game.

    >>> import gcge.player
    >>> import gcge.cards
    >>> p = gcge.player.Player('some_id', 'Quixote')
    >>> print( len(p.hand) )
    0
    >>> c = gcge.cards.Card('foo')
    >>> p.giveCard(c)
    >>> print( len(p.hand) )
    1
    >>> p.takeCard(c)
    >>> print( len(p.hand) )
    0
    >>> p.takeCard(c)
    Traceback (most recent call last):
    ...
    ValueError: list.remove(x): x not in list
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.hand = []

    def giveCard(self,card):
        self.hand.append(card)

    def takeCard(self,card):
        self.hand.remove(card)
