#!/usr/bin/env python
# coding: utf-8

# ### Zipping

# We've already used the `zip` function quite a bit.
# 
# It zips up two iterables and yields tuples containing elements from all iterables in "parallel". It is also lazy, and it will stop once the first iterable is exhausted.
# 
# Let's look at a simple example:

# In[1]:


l1 = [1, 2, 3, 4, 5]
l2 = [1, 2, 3, 4]
l3 = [1, 2, 3]


# In[2]:


list(zip(l1, l2, l3))


# As you can see, the shortest iterable we provided to the `zip` function had a length of 3 (so it reached the end of iteration first), and our output therefore only had 3 tuples in it.
# 
# Of course, this works with iterators and generators too:

# In[3]:


def integers(n):
    for i in range(n):
        yield i
        
def squares(n):
    for i in range(n):
        yield i**2
        
def cubes(n):
    for i in range(n):
        yield i**3


# In[4]:


iter1 = integers(6)
iter2 = squares(5)
iter3 = cubes(4)


# In[5]:


list(zip(iter1, iter2, iter3))


# Sometimes we want to zip up iterables but completely iterate all the iterables, and not stop at the shortest. Of course, the problem is what to do with iterables that have been fully iterated before the longest one has?
# 
# Simple, we just need to provide a default "filler" value.
# 
# And that's how the `zip_longest` function from `itertools` works:

# In[6]:


from itertools import zip_longest


# In[7]:


help(zip_longest)


# As you can see, we can only specify a single default value, this means that default will be used for any provided iterable once it has been fully iterated.
# 
# As expected, `zip_longest` yields its values - it is lazy.
# 
# Let's see an example:

# In[8]:


l1 = [1, 2, 3, 4, 5]
l2 = [1, 2, 3, 4]
l3 = [1, 2, 3]


# In[9]:


list(zip_longest(l1, l2, l3, fillvalue='N/A'))


# Of course, since this zips over the longest iterable, beware of using an infinite iterable!
# 
# You don't have to worry about this with the normal `zip` function as long as at least one of the iterables is finite:

# In[10]:


def squares():
    i = 0
    while True:
        yield i ** 2
        i += 1

def cubes():
    i = 0
    while True:
        yield i ** 3
        i += 1


# Obviously `squares` produces an inifinite iterator. But we can still zip it with a finite iterable:

# In[11]:


iter1 = squares()
iter2 = cubes()
list(zip(range(10), iter1, iter2))


# Don't try the same thing with `zip_longest`!
