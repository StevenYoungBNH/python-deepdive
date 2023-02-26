#!/usr/bin/env python
# coding: utf-8

# ### Custom Sequences (Part 1)

# We'll focus first on how to create a custom sequence type that supports indexing, slicing (read only) and iteration. We'll look into mutable custom sequences in an upcoming video.

# First we should understand how the `__getitem__` method works for iteration and retrieving individual elements from a sequence:

# In[2]:


my_list = [0, 1, 2, 3, 4, 5]


# In[3]:


my_list.__getitem__(0)


# In[4]:


my_list.__getitem__(5)


# But if our index is out of bounds:

# In[5]:


my_list.__getitem__(6)


# we get an IndexError.

# Technically, the `list` object's `__getitem__` method also supports negative indexing and slicing:

# In[6]:


my_list.__getitem__(-1)


# In[7]:


my_list.__getitem__(slice(0,6,2))


# In[8]:


my_list.__getitem__(slice(None, None, -1))


# #### Mimicking Python's `for` loop using the `__getitem__` method

# In[9]:


my_list = [0, 1, 2, 3, 4, 5]


# In[10]:


for item in my_list:
    print(item ** 2)


# Now let's do the same thing ourselves without a for loop:

# In[11]:


index = 0
while True:
    try:
        item = my_list.__getitem__(index)
    except IndexError:
        # reached the end of the sequence
        break
    # do something with the item...
    print(item ** 2)
    index += 1


# #### Implementing a custom Sequence 

# Custom objects can support slicing - we'll see this later in this course, but for now we'll take a quick peek ahead.
# 
# To make a custom classes support indexing (and slicing) we only need to implement the `__getitem__` method which receives the index (or slice) we are interested in.

# In[12]:


class MySequence:
    def __getitem__(self, index):
        print(type(index), index)


# In[13]:


my_seq = MySequence()


# In[14]:


my_seq[0]


# In[15]:


my_seq[100]


# In[16]:


my_seq[0:2]


# In[17]:


my_seq[0:10:2]


# As you can see, the `__getitem__` method receives an index number of type `int` when we use `[n]` and a `slice` object when we use `[i:j]` or `[i:j:k]`.

# As we saw in a previous lecture, given the bounds for a slice, and the length of the sequence we are slicing, we can always define a `range` that will generate the desired indices.
# 
# We also saw that the `slice` object has a method, `indices`, that precisely tells us the start/stop/step values we would need for an equivalent `range`, given the length of the sequence we are slicing.
# 
# Let's recall a simple example first:

# In[18]:


l = 'python'
len(l)


# In[19]:


s = slice(0, 6, 2)
l[s]


# In[20]:


s.start, s.stop, s.step


# In[21]:


s.indices(6)


# In[22]:


list(range(0, 6, 2))


# This matches exactly the indices that were selected from the sequence `'python'`

# ### Example

# So, why am I re-emphasizing this equivalence between the indices in a `slice` and and equivalent `range` object?

# Let's say we want to implement our own sequence type and we want to support slicing.

# For this example we'll create a custom Fibonacci sequence type.

# First recall that the `__getitem__` will receive either an integer (for simple indexing), or a slice object:

# In[23]:


class Fib:
    def __getitem__(self, s):
        print(type(s), s)


# In[24]:


f = Fib()
f[2]
f[2:10:2]


# We'll use that to implement both indexing and slicing for our custom Fibonacci sequence type.

# We'll make our sequence type bounded (i.e. we'll have to specify the size of the sequence). But we are not going to pre-generate the entire sequence of Fibonacci numbers, we'll only generate the ones that are being requested as needed.

# In[25]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            print(f'requesting [{s}]')
        else:
            # slice being requested
            print(f'requesting [{s.start}:{s.stop}:{s.step}]')


# In[26]:


f = Fib(10)


# In[27]:


f[3]


# In[28]:


f[:5]


# Let's now add in what the equivalent range would be:

# In[29]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            print(f'requesting [{s}]')
        else:
            # slice being requested
            print(f'requesting [{s.start}:{s.stop}:{s.step}]')
            idx = s.indices(self._n)
            rng = range(*idx)
            print(f'\trange({idx[0]}, {idx[1]}, {idx[2]}) --> {list(rng)}')


# In[30]:


f = Fib(10)
f[3:5]
f[::-1]


# Next step is for us to actually calculate the n-th Fibonacci number, we'll use memoization as well (see lecture on decorators and memoization if you need to refresh your memory on that):

# In[31]:


from functools import lru_cache


# In[32]:


@lru_cache(2**10)
def fib(n):
    if n < 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)


# In[33]:


fib(0), fib(1), fib(2), fib(3), fib(4), fib(5), fib(50)


# Now, let's make this function part of our class:

# In[34]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            print(f'requesting [{s}]')
        else:
            # slice being requested
            print(f'requesting [{s.start}:{s.stop}:{s.step}]')
            idx = s.indices(self._n)
            rng = range(idx[0], idx[1], idx[2])
            print(f'\trange({idx[0]}, {idx[1]}, {idx[2]}) --> {list(rng)}')
    
    @staticmethod
    @lru_cache(2**32)
    def _fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)


# The next step is to implement the `__getitem__` method. Let's start by implementing the simple indexing:

# In[35]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            return self._fib(s)
        else:
            # slice being requested
            print(f'requesting [{s.start}:{s.stop}:{s.step}]')
            idx = s.indices(self._n)
            rng = range(idx[0], idx[1], idx[2])
            print(f'\trange({idx[0]}, {idx[1]}, {idx[2]}) --> {list(rng)}')
            
    @staticmethod
    @lru_cache(2**32)
    def _fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)


# Let's test that out:

# In[36]:


f = Fib(100)


# In[37]:


f[0], f[1], f[2], f[3], f[4], f[5], f[50]


# But we still have a few problems.
# 
# First we do not handle negative values, and we also will return results for indices that should technically be out of bounds, so we can't really iterate through this sequence yet as we would end up with an infinite iteration!

# In[38]:


f[200], f[-5]


# So we first need to raise an `IndexError` exception when the index is out of bounds, and we also need to remap negative indices (for example `-1` should correspond to the last element of the sequence, and so on)

# In[39]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            if s < 0:
                s = self._n + s
            if s < 0 or s > self._n - 1:
                raise IndexError
            return self._fib(s)
        else:
            # slice being requested
            print(f'requesting [{s.start}:{s.stop}:{s.step}]')
            idx = s.indices(self._n)
            rng = range(idx[0], idx[1], idx[2])
            print(f'\trange({idx[0]}, {idx[1]}, {idx[2]}) --> {list(rng)}')
            
    @staticmethod
    @lru_cache(2**32)
    def _fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)


# In[40]:


f = Fib(10)


# In[41]:


f[9], f[-1]


# In[42]:


f[10]


# In[43]:


f[-100]


# In[44]:


for item in f:
    print(item)


# We still don't support slicing though...

# In[45]:


f[0:2]


# So let's implement slicing as well:

# In[46]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            if s < 0:
                s = self._n + s
            if s < 0 or s > self._n - 1:
                raise IndexError
            return self._fib(s)
        else:
            # slice being requested
            idx = s.indices(self._n)
            rng = range(idx[0], idx[1], idx[2])
            return [self._fib(n) for n in rng]
            
    @staticmethod
    @lru_cache(2**32)
    def _fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)


# In[47]:


f = Fib(10)


# In[48]:


f[0:5]


# In[49]:


f[5::-1]


# In[50]:


list(f)


# In[51]:


f[::-1]


# One other thing, is that the built-in `len` function will not work with our class:

# In[52]:


f = Fib(10)


# In[53]:


len(f)


# That's an easy fix, we just need to implement the `__len__` method:

# In[54]:


class Fib:
    def __init__(self, n):
        self._n = n
    
    def __len__(self):
        return self._n
    
    def __getitem__(self, s):
        if isinstance(s, int):
            # single item requested
            if s < 0:
                s = self._n + s
            if s < 0 or s > self._n - 1:
                raise IndexError
            return self._fib(s)
        else:
            # slice being requested
            idx = s.indices(self._n)
            rng = range(idx[0], idx[1], idx[2])
            return [self._fib(n) for n in rng]
            
    @staticmethod
    @lru_cache(2**32)
    def _fib(n):
        if n < 2:
            return 1
        else:
            return fib(n-1) + fib(n-2)


# In[55]:


f = Fib(10)


# In[56]:


len(f)


# One thing I want to point out here: we did not need to use inheritance! There was no need to inherit from another sequence type. All we really needed was to implement the `__getitem__` and `__len__` methods.

# The other thing I want to mention, is that I would not use recursion for production purposes for a Fibonacci sequence, even with memoization - partly because of the cost of recursion and the limit to the recursion depth that is possible.
# 
# Also, when we look at generators, and more particularly generator expressions, we'll see better ways of doing this as well.
# 
# I really wanted to show you a simple example of how to create your own sequence types.
