from collections import namedtuple
import pprint


Card = namedtuple('Card', 'rank, suit')
SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
RANKS = tuple(range(2, 11)) + tuple('JQKA')


def card_gen():
    for i in range(len(SUITS) * len(RANKS)):
        suit = SUITS[i // len(RANKS)]
        rank = RANKS[i % len(RANKS)]
        card = Card(rank, suit)
        yield card


for card in card_gen():
    print(card)

del(SUITS)
del(RANKS)


class CardDeck:
    SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    RANKS = tuple(range(2, 11)) + tuple('JQKA')

    def __iter__(self):
        return CardDeck.card_gen()

    @staticmethod
    def card_gen():
        for suit in CardDeck.SUITS:
            for rank in CardDeck.RANKS:
                card = Card(rank, suit)
                yield card


deck = CardDeck()
print("\n\n\n1st time")
pprint.pprint([card for card in deck])
print("\n\n\n2nd time")
pprint.pprint([card for card in deck])


class CardDeck:
    SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    RANKS = tuple(range(2, 11)) + tuple('JQKA')

    def __iter__(self):
        return CardDeck.card_gen()

    def __reversed__(self):
        return CardDeck.reversed_card_gen()

    @staticmethod
    def card_gen():
        for suit in CardDeck.SUITS:
            for rank in CardDeck.RANKS:
                card = Card(rank, suit)
                yield card

    @staticmethod
    def reversed_card_gen():
        for suit in reversed(CardDeck.SUITS):
            for rank in reversed(CardDeck.RANKS):
                card = Card(rank, suit)
                yield card


deck = CardDeck()
r = deck.__reversed__()
rdeck = reversed(deck)
print("\n\n\n1st time")
pprint.pprint([card for card in rdeck])
print("\n\n\n2nd time")
pprint.pprint([card for card in r])
