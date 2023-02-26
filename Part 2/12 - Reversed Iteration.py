# Sometimes we may want to iterate through an iterable but in reverse order.
# Of course, this means the collection being iterated must be finite.
# Python has a built-in function called reversed() to do this that will work with any type that implement the sequence
# protocol. But for iterables in general it's a little more complicated.
# Let's first build a custom iterable.
# For this example we are going to build a custom iterable that returns cards from a 52-card deck.
# The deck will be in order of suits (Spades, Hearts, Diamonds and Clubs) and card values (from 2 (lowest) to Ace (highest)).
# We are going to use lazy loading - i.e. we are not going to pre-build our card deck.
# We just need to recognize that each suit contains 13 cards, so an integer division of the index of the card in the deck
# will tell us which suit it is. But of course we start indexing at 0.

# Example
# If the requested card is the 6th in the deck (i.e. index = 5):
# 5 // 13 = 0 ==> first suit (Spades)
# If the requested card is the 13th in the deck (i.e. index = 12):
# 12 // 13 = 0 ==> first suit (Spades)
# If the requested card is the 14th in the deck (i.e. index = 13):
# 13 // 13 = 1 ==> second suit (Hearts)
# To determine which card in the suit we are interested in, we simply need to use the % operator, again recognizing that
# there are 13 cards in each suit:
# Example
# If the requested card is the 6th in the deck (i.e. index = 5):
# 5 % 13 = 5 ==> 5th card in the suit
# If the requested card is the 13th in the deck (i.e. index = 12):
# 12 % 13 = 12 ==> 12th card in the suit
# If the requested card is the 14th in the deck (i.e. index = 13):
# 13 % 13 = 0 ==> 1st card in the suit

from collections import namedtuple
_SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
_RANKS = tuple(range(2, 11)) + tuple('JQKA')

Card = namedtuple('Card', 'rank suit')


_SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
_RANKS = tuple(range(2, 11)) + tuple('JQKA')

Card = namedtuple('Card', 'rank suit')


class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)

    # def __len__(self):
        # return self.length

    def __iter__(self):
        return self.CardDeckIterator(self.length)
        # return self.CardDeckIterator(self)

    class CardDeckIterator:
        def __init__(self, length):
            self.length = length
            self.i = 0

        def __iter__(self, length):
            print('__iter__ called')
            return self

        def __next__(self):
            print('__next__ called')
            if self.i >= self.length:
                raise StopIteration
            else:
                suit = _SUITS[self.i // len(_RANKS)]
                rank = _RANKS[self.i % len(_RANKS)]
                self.i += 1
            return Card(rank, suit)


deck = CardDeck()

for card in deck:
    print(card)


class CardDeck:
    def __init__(self):
        self.length = len(_SUITS) * len(_RANKS)

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.CardDeckIterator(self.length)

    class CardDeckIterator:
        def __init__(self, length):
            self.length = length
            self.i = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                suit = _SUITS[self.i // len(_RANKS)]
                rank = _RANKS[self.i % len(_RANKS)]
                self.i += 1
                return Card(rank, suit)
