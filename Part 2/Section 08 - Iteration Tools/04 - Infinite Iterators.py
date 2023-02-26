#!/usr/bin/env python
# coding: utf-8

# ### Infinite Iterators

# There are three functions in the `itertools` module that produce infinite iterators: `count`, `cycle` and `repeat`.

# In[1]:


from itertools import (
    count,
    cycle,
    repeat, 
    islice)


# #### count

# The `count` function is similar to range, except it does not have a `stop` value. It has both a `start` and a `step`:

# In[2]:


g = count(10)


# In[3]:


list(islice(g, 5))


# In[4]:


g = count(10, step=2)


# In[5]:


list(islice(g, 5))


# And so on. 
# 
# Unlike the `range` function, whose arguments must always be integers, `count` works with floats as well:

# In[6]:


g = count(10.5, 0.5)


# In[7]:


list(islice(g, 5))


# In fact, we can even use other data types as well:

# In[8]:


g = count(1+1j, 1+2j)


# In[9]:


list(islice(g, 5))


# We can even use Decimal numbers:

# In[10]:


from decimal import Decimal


# In[11]:


g = count(Decimal('0.0'), Decimal('0.1'))


# In[12]:


list(islice(g, 5))


# ### Cycle

# `cycle` is used to repeatedly loop over an iterable:

# In[13]:


g = cycle(('red', 'green', 'blue'))


# In[14]:


list(islice(g, 8))


# One thing to note is that this works **even** if the argument is an iterator (i.e. gets exhausted after the first complete iteration over it)!

# Let's see a simple example of this:

# In[15]:


def colors():
    yield 'red'
    yield 'green'
    yield 'blue'


# In[16]:


cols = colors()


# In[17]:


list(cols)


# In[18]:


list(cols)


# As expected, `cols` was exhausted after the first iteration.
# 
# Now let's see how `cycle` behaves:

# In[19]:


cols = colors()
g = cycle(cols)


# In[20]:


list(islice(g, 10))


# As you can see, `cycle` iterated over the elements of iterator, and continued the iteration even though the first run through the iterator technically exhausted it.

# ##### Example

# A simple application of `cycle` is dealing a deck of cards into separate hands:

# In[21]:


from collections import namedtuple


# In[22]:


Card = namedtuple('Card', 'rank suit')


# In[23]:


def card_deck():
    ranks = tuple(str(num) for num in range(2, 11)) + tuple('JQKA')
    suits = ('Spades', 'Hearts', 'Diamonds', 'Clubs')
    for suit in suits:
        for rank in ranks:
            yield Card(rank, suit)


# Assume we want 4 hands, so we can think of the hands as a list containing 4 elements - each of which is itself a list containing cards.
# 
# The indices of the hands would be `0, 1, 2, 3` in the hands list:

# We could certainly do it this way:

# In[24]:


hands = [list() for _ in range(4)]


# In[25]:


hands


# In[26]:


index = 0
for card in card_deck():
    index = index % 4
    hands[index].append(card)
    index += 1


# In[27]:


hands


# You notice how we had to use the `mod` operator and an `index` to **cycle** through the hands.
# 
# So, we can use the `cycle` function instead:

# In[28]:


hands = [list() for _ in range(4)]


# In[29]:


index_cycle = cycle([0, 1, 2, 3])
for card in card_deck():
    hands[next(index_cycle)].append(card)


# In[30]:


hands


# But we really can simplify this even further - why are we cycling through the indices? Why not simply cycle through the hand themselves, and append the card to the hands?

# In[31]:


hands = [list() for _ in range(4)]


# In[32]:


hands_cycle = cycle(hands)
for card in card_deck():
    next(hands_cycle).append(card)


# In[33]:


hands


# #### Repeat

# The `repeat` function is used to create an iterator that just returns the same value again and again. By default it is infinite, but a count can be specified optionally:

# In[34]:


g = repeat('Python')
for _ in range(5):
    print(next(g))


# And we also optionally specify a count to make the iterator finite:

# In[35]:


g = repeat('Python', 4)


# In[36]:


list(g)


# The important thing to note as well, is that the "value" that is returned is the **same** object every time!

# Let's see this:

# In[37]:


l = [1, 2, 3]


# In[38]:


result = list(repeat(l, 3))


# In[39]:


result


# In[40]:


l is result[0], l is result[1], l is result[2]


# So be careful here. If you try to use repeat to create three separate instances of a list, you'll actually end up with shared references:

# In[41]:


result[0], result[1], result[2]


# In[42]:


result[0][0] = 100


# In[43]:


result[0], result[1], result[2]


# If you want to end up with three separate copies of your argument, then you'll need to use a copy mechanism (either shallow or deep depending on your needs).
# 
# This is easily done using a comprehension expression:

# In[44]:


l = [1, 2, 3]
result = [item[:] for item in repeat(l, 3)]


# In[45]:


result


# In[46]:


l is result[0], l is result[1], l is result[2]


# In[47]:


result[0][0] = 100


# In[48]:


result

