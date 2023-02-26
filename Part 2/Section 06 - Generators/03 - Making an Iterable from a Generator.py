#!/usr/bin/env python
# coding: utf-8

# ### Making an Iterable from a Generator

# As we now know, generators are iterators.
# 
# This means that they become exhausted - so sometimes we want to create an iterable instead.
# 
# There's no magic here, we simply have to implement a class that implements the iterable protocol:

# Let's write a simple generator that generates the squares of integers:

# In[1]:


def squares_gen(n):
    for i in range(n):
        yield i ** 2


# Now, we can create a new generator:

# In[2]:


sq = squares_gen(5)


# In[3]:


for num in sq:
    print(num)


# But, `sq` was an iterator - so now it's been exhausted:

# In[4]:


next(sq)


# To restart the iteration we have to create a new instance of the generator (iterator):

# In[5]:


sq = squares_gen(5)


# In[6]:


[num for num in sq]


# So, let's wrap this in an iterable:

# In[7]:


class Squares:
    def __init__(self, n):
        self.n = n
        
    def __iter__(self):
        return squares_gen(self.n)


# In[8]:


sq = Squares(5)


# In[9]:


[num for num in sq]


# And we can do it again:

# In[10]:


[num for num in sq]


# We can put those pieces of code together if we prefer:

# In[11]:


class Squares:
    def __init__(self, n):
        self.n = n
        
    @staticmethod
    def squares_gen(n):
        for i in range(n):
            yield i ** 2
        
    def __iter__(self):
        return Squares.squares_gen(self.n)


# In[12]:


sq = Squares(5)


# In[13]:


[num for num in sq]


# #### Generators used with other Generators

# I want to point out that you can also easily run into various bugs when you use generators with other generator functions.
# 
# Consider this example:

# In[14]:


def squares(n):
    for i in range(n):
        yield i ** 2


# In[15]:


sq = squares(5)


# In[16]:


enum_sq = enumerate(sq)


# Now `enumerate` is lazy, so `sq` had not, at this point, been consumed:

# In[17]:


next(sq)


# In[18]:


next(sq)


# Since we have consumed two elements from `sq`, when we now use `enumerate` it will have two less elements from sq:

# In[19]:


next(enum_sq)


# You'll notice that we don't get the first element of the original `sq` - instead we get the third element (`2 ** 2`).
# 
# Moreover, you'll notice that the index returned in the tuple produced by `enumerate` is 0, not 2!
