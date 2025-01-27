#!/usr/bin/env python
# coding: utf-8

# ### Example: Card Deck

# Let's go back to a previous example we worked with, our card deck.
# 
# Let's rebuild it quickly, but this time using generators instead of a custom iterator:

# In[1]:


from collections import namedtuple

Card = namedtuple('Card', 'rank, suit')
SUITS = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
RANKS = tuple(range(2, 11)) + tuple('JQKA')


# Recall how we recovered the suit and rank for any given card index in the deck (assuming the sorting is `2S...AS  2H...AH  2D...AD  2C...AC`):
# 
# ```
# suit_index = card_index // len(RANKS)
# rank_index = card_index % len(RANKS)
# ```

# In[2]:


def card_gen():
    for i in range(len(SUITS) * len(RANKS)):
        suit = SUITS[i // len(RANKS)]
        rank = RANKS[i % len(RANKS)]
        card = Card(rank, suit)
        yield card


# So now we can iterate using our generator:

# In[3]:


for card in card_gen():
    print(card)


# But we can really simplify this further!
# 
# We don't have to use these indices at all!

# In[4]:


def card_gen():
    for suit in SUITS:
        for rank in RANKS:
            card = Card(rank, suit)
            yield card


# And we now have the same functionality:

# In[5]:


for card in card_gen():
    print(card)


# We can now make it into an iterable:

# In[6]:


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
        


# In[7]:


deck = CardDeck()


# In[8]:


[card for card in deck]


# And of course we can do it again:

# In[9]:


[card for card in deck]


# One thing we don't have here is the support for `reversed`:

# In[10]:


reversed(CardDeck())


# But we can add it in by implementing the `__reversed__` method and returning an iterator that iterates the deck in reverse order.

# In[11]:


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


# In[12]:


rev = reversed(CardDeck())


# In[13]:


[card for card in rev]

