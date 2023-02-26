#!/usr/bin/env python
# coding: utf-8

# ### Combinatorics

# There are a number of functions in `itertools` that are concerned with thing like permutations and combinations.
# 
# Let's look at each one briefly - I am not going to go into much depth as to what permutations and combinations are though - this is not meant to be a statistics course :-)

# In[1]:


import itertools


# #### Cartesian Product

# The cartesian product is actually a lot more useful than it might appear at first.
# 
# Consider this example, where we want to create a multiplication table as we have seen before:

# In[2]:


def matrix(n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            yield f'{i} x {j} = {i*j}'


# We can look at a few elements using `islice`:

# In[3]:


list(itertools.islice(matrix(10), 10, 20))


# Notice that we iterated through the same sets (the numbers from 1 to 10) in a nested fashion.
# 
# If we think of those two sets as 
# $$
# s1 = \{1, 2, 3, ..., 10\}
# $$
# $$
# s2 = \{1, 2, 3, ..., 10\}
# $$
# then the Cartesian product of the two sets is:
# $$
# s_1 \times s_2 = \{(x_1, x_2) \, \vert \, x_1 \in s_1 \, \textrm{and} \, x_2 \in s_2\}
# $$

# Another way to think of it is by creating a table (just like our multiplication table!):
# 
# ```
#         y1        y2        y3
# x1  (x1, y1)  (x1, y2)  (x1, y3)
# 
# x2  (x2, y1)  (x2, y2)  (x2, y3)
# 
# x3  (x3, y1)  (x3, y2)  (x3, y3)
# 
# x4  (x4, y1)  (x4, y2)  (x4, y3)
# ```

# Our multiplication table was just the product of $x_i$ and $y_i$:

# ```
#        y1       y2       y3      y4
# x1  x1 * y1  x1 * y2  x1 * y3  x1 * y4
# 
# x2  x2 * y1  x2 * y2  x2 * y3  x2 * y4  
# 
# x3  x3 * y1  x3 * y2  x3 * y3  x3 * y4  
# 
# x4  x4 * y1  x4 * y2  x4 * y3  x4 * y4  
# ```

# So, the Cartesian product of two iterables in general can be generated using a nested loop:

# In[4]:


l1 = ['x1', 'x2', 'x3', 'x4']
l2 = ['y1', 'y2', 'y3']
for x in l1:
    for y in l2:
        print((x, y), end=' ')
    print('')


# We can achieve the same result with the `product` function in `itertools`. As usual, it is lazy as well.

# In[5]:


l1 = ['x1', 'x2', 'x3', 'x4']
l2 = ['y1', 'y2', 'y3']
list(itertools.product(l1, l2))


# As a simple example, let's go back to the multiplication table we created using a generator function.

# In[6]:


def matrix(n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            yield (i, j, i*j)


# In[7]:


list(matrix(4))


# In[8]:


def matrix(n):
    for i, j in itertools.product(range(1, n+1), range(1, n+1)):
        yield (i, j, i*j)


# In[9]:


list(matrix(4))


# And of course this is now simple enough to even use just a generator expression:

# In[10]:


def matrix(n):
    return ((i, j, i*j) 
            for i, j in itertools.product(range(1, n+1), range(1, n+1)))


# In[11]:


list(matrix(4))


# You'll notice how we repeated the `range(1, n+1)` twice?
# 
# This is a great example of where `tee` can be useful:

# In[12]:


from itertools import tee

def matrix(n):
    return ((i, j, i*j) 
            for i, j in itertools.product(*itertools.tee(range(1, n+1), 2)))


# In[13]:


list(matrix(4))


# #### Example 1

# A common usage of Cartesian products might be to generate a grid of coordinates.
# 
# For a 2D space for example, we might want to generate a grid of points ranging from -5 to 5 in both the x and y axes, with a step of 0.5.
# 
# We can't use a range since ranges need integral numbers, but we have the `count` function in itertools we have seen before:

# In[14]:


def grid(min_val, max_val, step, *, num_dimensions=2):
    axis = itertools.takewhile(lambda x: x <= max_val,
                               itertools.count(min_val, step))
    
    # to handle multiple dimensions, we just need to repeat the axis that
    # many times - tee is perfect for that
    axes = itertools.tee(axis, num_dimensions)

    # and now we just need the product of all these iterables
    return itertools.product(*axes)


# In[15]:


list(grid(-1, 1, 0.5))


# And of course we can now do it in 3D as well:

# In[16]:


list(grid(-1, 1, 0.5, num_dimensions=3))


# #### Example 2

# Another simple application of this might be to determine the odds of rolling an 8 with a pair of dice (with values 1 - 6).
# 
# We can brute force this by generating all the possible results (the sample space), and counting how may items add up to 8.
# 
# Let's break it up into a few steps:

# In[17]:


sample_space = list(itertools.product(range(1, 7), range(1, 7)))
print(sample_space)


# Now we want to filter out the tuples whose elements add up to 8:

# In[18]:


outcomes = list(filter(lambda x: x[0] + x[1] == 8, sample_space))
print(outcomes)


# And we can calculate the odds by dividing the number acceptable outcomes by the size of the sample space. I'll actually use a `Fraction` so we retain our result as a rational number:

# In[19]:


from fractions import Fraction
odds = Fraction(len(outcomes), len(sample_space))
print(odds)


# #### Permutations

# From Wikipedia: 
# 
# 
# > In mathematics, the notion of permutation relates to the act of arranging all the members of a set into some sequence or order, or if the set is already ordered, rearranging (reordering) its elements, a process called permuting. These differ from combinations, which are selections of some members of a set where order is disregarded.
# 
# 
# https://en.wikipedia.org/wiki/Permutation

# We can create permutations of length n from an iterable of length m (n <= m) using the `permutation` function:

# In[20]:


l1 = 'abc'
list(itertools.permutations(l1))


# As you can see all the permutations are, by default, the same length as the original iterable.
# 
# We can create permutations of smaller length by specifying the `r` value:

# In[21]:


list(itertools.permutations(l1, 2))


# The important thing to note is that elements are not 'repeated' in the permutation. The uniqueness of an element is **not** based on its value, but rather on its **position** in the original iterable.
# 
# Take this example:

# In[22]:


list(itertools.permutations('aaa'))


# This means that the following will yield what looks like the same permutations when considering the **values** of the iterable:

# In[23]:


list(itertools.permutations('aba', 2))


# As you can see, each tuple looks like it has been repeated twice - but considering the elements are unique based on their position, this is actually quite correct.

# #### Combinations

# From Wikipedia:
# >Combinations refer to the combination of n things taken k at a time without repetition. To refer to combinations in which repetition is allowed, the terms k-selection,[1] k-multiset,[2] or k-combination with repetition are often used.
# 
# https://en.wikipedia.org/wiki/Combination

# `itertools` offers both flavors - with and without replacement.
# 
# Let's look at a simple example with replacement first:

# In[24]:


list(itertools.combinations([1, 2, 3, 4], 2))


# As you can see `(4, 3)` is not included in the result since, as a combination, it is the same as `(3, 4)` - order is not important.

# If we want replacement:

# In[25]:


list(itertools.combinations_with_replacement([1, 2, 3, 4], 2))


# #### Example 3

# A simple application of this might be to calculate the odds of pulling four consecutive aces from a deck of 52 cards.
# 
# That's very easy to figure out, but we could use a brute force approach by calculating all the 4-combinations (without repetition) from a deck of 52 cards.
# 
# Let's try it:

# First we need a deck:

# In[26]:


SUITS = 'SHDC'
RANKS = tuple(map(str, range(2, 11))) + tuple('JQKA')


# In[27]:


RANKS


# I wanted all the elements in my `RANKS` to be strings - just to have a consistent data type, and to show you how handy `map` can be!

# Next I need to create the deck:

# In[28]:


deck = [rank + suit for suit in SUITS for rank in RANKS]


# In[29]:


deck[0:5]


# Hmm... A nested loop. Maybe `product` would work well here!

# In[30]:


deck = [rank + suit for suit, rank in itertools.product(SUITS, RANKS)]


# I would much prefer having a named tuple for the deck, so let's do that as well:

# In[31]:


from collections import namedtuple
Card = namedtuple('Card', 'rank suit')


# In[32]:


deck = [Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS)]


# And I really don't need it as a list - a generator expression will do just as well...

# In[33]:


deck = (Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS))


# Next we need to produce our sample space - all combinations of 4 cards from the deck, without repetition:

# In[34]:


sample_space = itertools.combinations(deck, 4)


# Next we need to count the number of acceptable outcomes - but we also need to count the size of our sample space.
# We can't use `len()` though - iterables in general don't support that method. 
# I could create the sample space twice, but that seems wasteful - so instead I'm going to iterate through the sample space once and just keep track of both counts:

# In[35]:


deck = (Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS))
sample_space = itertools.combinations(deck, 4)
total = 0
acceptable = 0
for outcome in sample_space:
    total += 1
    for card in outcome:
        if card.rank != 'A':
            break
    else:
        # else block is executed if loop terminated without a break
        acceptable += 1
print(f'total={total}, acceptable={acceptable}')
print('odds={}'.format(Fraction(acceptable, total)))
print('odds={:.10f}'.format(acceptable/total))


# We can easily verify that this is correct:

# Odds of succesively picking four aces from a shuffled deck is:
# 
# $$
# \frac{4}{52} \times \frac{3}{51} \times \frac{2}{50} \times \frac{1}{49}
# = \frac{24}{6497400} = \frac{1}{270725}
# $$

# I also want to point out that we could use the `all` function instead of that inner `for` loop and the `else` block.
# 
# Remember that `all(iterable)` will evaluate to True if all the elements of the iterable are truthy.
# Now in our case, since ranks are non-empty strings, they will always be truthy, so we can't use `all` directly:

# In[36]:


all(['A', 'A', '10', 'J'])


# Instead we can use the `map` function, yet again!, to test if the value is an 'A' or not:

# In[37]:


l1 = ['K', 'A', 'A', 'A']
l2 = ['A', 'A', 'A', 'A']

print(list(map(lambda x: x == 'A', l1)))
print(list(map(lambda x: x == 'A', l2)))


# So now we can use `all` (and we don't have to create a list):

# In[38]:


print(all(map(lambda x: x == 'A', l1)))
print(all(map(lambda x: x == 'A', l2)))


# So, we could rewrite our algorithm as follows:

# In[39]:


deck = (Card(rank, suit) for suit, rank in itertools.product(SUITS, RANKS))
sample_space = itertools.combinations(deck, 4)
total = 0
acceptable = 0
for outcome in sample_space:
    total += 1
    if all(map(lambda x: x.rank == 'A', outcome)):
        acceptable += 1

print(f'total={total}, acceptable={acceptable}')
print('odds={}'.format(Fraction(acceptable, total)))
print('odds={:.10f}'.format(acceptable/total))


# In[ ]:




