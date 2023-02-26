#!/usr/bin/env python
# coding: utf-8

# ### Generator States

# Let's look at a simple generator function:

# In[34]:


def gen(s):
    for c in s:
        yield c


# We create an generator object by calling the generator function:

# In[35]:


g = gen('abc')


# At this point the generator object is **created**, but we have not actually started running it. To do so, we call `next()`, which then starts running the function body until the first `yield` is encountered:

# In[36]:


next(g)


# Now the generator is **suspended**, waiting for us to call next again:

# In[37]:


next(g)


# Every time we call `next`, the generator function runs, or is in a **running** state until the next yield is encountered, or no more results are yielded and the function actually returns:

# In[38]:


next(g)


# In[39]:


next(g)


# Once we exhaust the generator, we get a `StopIteration` exception, and we can think of the generator as being **closed**.

# As we can see, a generator can be in one of four states:
# 
# * created
# * running
# * suspended
# * closed

# We can actually request the state of a generator programmatically by using the `inspect` module's `getgeneratorstate()` function:

# In[33]:


from inspect import getgeneratorstate


# In[46]:


g = gen('abc')


# In[47]:


getgeneratorstate(g)


# We can start running the generator by calling `next`:

# In[48]:


next(g)


# And the state is now:

# In[49]:


getgeneratorstate(g)


# Once we exhaust the generator:

# In[50]:


next(g), next(g), next(g)


# The generator is now in a closed state:

# In[51]:


getgeneratorstate(g)


# Now we haven't seen the running state - to do that we just need to print the state from inside the generator - but to do that we need to have a reference to the generator object itself. This is not that easy to do, so I'm going to cheat and assume that the generator object will be referenced by a global variable `global_gen`:

# In[52]:


def gen(s):
    for c in s:
        print(getgeneratorstate(global_gen))
        yield c


# In[53]:


global_gen = gen('abc')


# In[54]:


next(global_gen)


# So a generator can be in these four very distinct states.
# 
# When the generator is created, it is not in a running or suspended state - it is simply in a **created** state.
# 
# We have to kick-off, or prime, the generator by calling `next` on it.
# 
# After the generator has yielded a value, it it is in **suspended** state.
# 
# Finally, once the generator **returns** (not yields), i.e. the StopIteration is raised, the generator is **closed**.

# Finally it is really important to understand that when a `yield` is encountered, the generator is suspended **exactly** at that point, but not before it has evaluated the expression to the right of the yield statement so it can produce that value in the return value of the `next()` function.
# 
# To see this, let's write a simple function and a generator function as follows:

# In[55]:


def square(i):
    print(f'squaring {i}')
    return i ** 2


# In[58]:


def squares(n):
    for i in range(n):
        yield square(i)
        print ('right after yield')


# In[59]:


sq = squares(5)


# In[60]:


next(sq)


# As you can see `square(i)` was evaluated, **then** the value was yielded, and the genrator was suspended exactly at the point the `yield` statement was encountered:

# In[61]:


next(sq)


# As you can see, only now does the `right after yield` string get printed from our generator.

# In[ ]:




