#!/usr/bin/env python
# coding: utf-8

# ### Slicing Iterables

# We know that sequence types can be sliced:
# sy 5/31/2022

# In[1]:


l = [1, 2, 3, 4, 5]


# In[2]:


l[0:2]


# Equivalently we can use the `slice` object:

# In[3]:


s = slice(0, 2)


# In[4]:


l[s]


# But this does not work with iterables that are not also sequence types:

# In[5]:


import math

def factorials(n):
    for i in range(n):
        yield math.factorial(i)


# In[6]:


facts = factorials(100)


# In[7]:


facts[0:2]


# But we could write a function to mimic this. Let's try a simplistic approach that will only work for a consecutive slice:

# In[8]:


def slice_(iterable, start, stop):
    for _ in range(0, start):
        next(iterable)
        
    for _ in range(start, stop):
        yield(next(iterable))


# In[9]:


list(slice_(factorials(100), 1, 5))


# This is quite simple, however we don't support a `step` value.

# The `itertools` module has a function, `islice` which implements this for us:

# In[10]:


list(factorials(10))


# Now let's use the `islice` function to obtain the first 3 elements:

# In[11]:


from itertools import islice


# In[12]:


islice(factorials(10), 0, 3)


# `islice` is itself a lazy iterator, so we can iterate through it:

# In[13]:


list(islice(factorials(10), 0, 3))


# We can even use a step value:

# In[16]:


list(islice(factorials(10), 1, 11, 2))


# It does not support negative indices, or step values, but it does support None for all the arguments. The default, as expected would then be the first element, the last element, and a step of 1:

# In[19]:


list(islice(factorials(10), None, None, 2))


# This function can be very useful when dealing with infinite iterators for example.

# In[20]:


def factorials():
    index = 0
    while True:
        yield math.factorial(index)
        index += 1


# Let's say we want to see the first 5 elements. We could do it the way we have up to now:

# In[22]:


facts = factorials()
for _ in range(50):
    print(next(facts))


# Or we could use `islice` as follows:

# In[23]:


list(islice(factorials(), 5))


# One thing to note is that `islice` is a lazy iterator, but when we use a `step` value, there is no magic, Python still has to call `next` on our iterable - it just doesn't always yield it back to us.
# 
# To see this, we'll add a print statement to our generator function:

# In[24]:


def factorials():
    index = 0
    while True:
        print(f'yielding factorial({index})...')
        yield math.factorial(index)
        index += 1


# In[25]:


list(islice(factorials(), 9))


# In[26]:


list(islice(factorials(), None, 10, 2))


# As you can see, even though 5 elements were yielded from `islice`, it still had to call our generator 10 times!

# The same thing happens if we skip elements in the slice, it still has to call next for the skipped elements:

# In[27]:


list(islice(factorials(), 5, 10))


# The other thing to watch out for is that islice is an **iterator** - which means it becomes exhausted, **even if you pass an iterable such as a list to it**!

# In[35]:


l = [1, 2, 3, 4, 5,6,7,8,9]


# In[36]:


s = islice(l, 0, 3)


# In[37]:


list(s)


# In[38]:


next(s)


# In[39]:


list(s)


# So watch out!

# Furthermore, keep in mind that `islice` iterates over our iterable in order to yield the appropriate values. This means that if we use an iterator, that iterator will get consumed, and possibly exhausted:

# In[40]:


facts = factorials()


# In[41]:


next(facts), next(facts), next(facts), next(facts)


# If we now start slicing `facts` with `islice`, remember that the first four values of `facts` have already been consumed!

# In[42]:


list(islice(facts, 0, 3))


# And of course, `islice` further consumed our iterator:

# In[43]:


next(facts)


# So, just something to keep in mind when we pass iterators to `islice`, and more generally to any of the functions in `itertools`.

# In[ ]:




