#!/usr/bin/env python
# coding: utf-8

# ### Yield From - Two-Way Communications

# In the last section on generators, we started looking at `yield from` and how we could delegate iteration to another iterator.
# 
# Let's see a simple example again:

# In[ ]:


def squares(n):
    for i in range(n):
        yield i ** 2


# In[2]:


def delegator(n):
    for value in squares(n):
        yield value


# In[3]:


gen = delegator(5)
for _ in range(5):
    print(next(gen))


# Alternatively we could write the same thing this way:

# In[4]:


def delegator(n):
    yield from squares(n)


# In[5]:


gen = delegator(5)
for _ in range(5):
    print(next(gen))


# **Terminology:** 
# When we use `yield from subgen` we are **delegating** to `subgen`.
# 
# The generator that delegates to the other generator is called the **delegator** and the generator that it delegates to is called the **subgenerator**.
# 
# So in our example `squares(n)` was the subgenerator, and `delegator()` was the delegator.
# 
# The context that contains the code making `next` calls to the delegator, is called the **caller's context**, or simply the **caller**.

# What is actually happening when we call
# ```
# next(gen)
# ```
# is that `gen` (the delegator) is passing along the `next` request to the `squares(n)` (the subgenerator).
# 
# In return, the subgenerator is yielding values back to the delegator, which in turn yields it back to us (the caller).
# 
# There is in fact a **two-way communication channel** established between the caller and the subgenerator - all because of `yield from`.
# 
# * caller: next --> delegator --> subgenerator
# * caller <-- delegator (yield) <-- subgenerator (yield)

# So, if `yield from` establishes this 2-way communication channel, and we can send `next` to the subgenerator via the delegator, can we send data using `send` as well?
# 
# The answer is yes. We'll take a look at this in some detail over the next few videos.
# 
# Let's start by looking at how the delegator works when a subgenerator closes by itself:

# We'll want to inspect the delegator and the subgenerator, so let's import what we'll need from the `inspect` module:

# In[6]:


from inspect import getgeneratorstate, getgeneratorlocals


# In[7]:


def song():
    yield "I'm a lumberjack and I'm OK"
    yield "I sleep all night and I work all day"


# In[8]:


def play_song():
    count = 0
    s = song()
    yield from s
    yield 'song finished'
    print('player is exiting...')


# Here `play_song` is the delegator, and `song` is the subgenerator. We, the Jupyter notebook, are the caller.

# In[9]:


player = play_song()


# In[10]:


print(getgeneratorstate(player))
print(getgeneratorlocals(player))


# As you can see, no local variables have been created in `player` yet - that's because it is created, not actually started.
# 
# Let's start it:

# In[11]:


next(player)


# Now let's look at the state of things:

# In[12]:


print(getgeneratorstate(player))
print(getgeneratorlocals(player))


# We can now get a handle to the subgenerator `s`:

# In[13]:


s = getgeneratorlocals(player)['s']


# And we can check the state of `s`:

# In[14]:


print(getgeneratorstate(s))


# As we can see the subgenerator is suspended.
# 
# Let's iterate a few more times:

# In[15]:


print(next(player))
print(getgeneratorstate(player))
print(getgeneratorstate(s))


# In[16]:


print(next(player))
print(getgeneratorstate(player))
print(getgeneratorstate(s))


# At this point the subgenerator exited, so its state is `GEN_CLOSED`, but the delegator (`player`) is just suspended, and in fact yielded `song finished`.
# 
# We can advance one more time:

# In[17]:


print(next(player))


# We get the `StopIteration` exception because `player` returned, and now both the delegator and the subgenerator are in a closed state:

# In[18]:


print(getgeneratorstate(player))
print(getgeneratorstate(s))


# Important to note here is that when the subgenerator returned, the delegator **continued running normally**.
# 
# Let's make a tweak to our `player` generator to make this even more evident:

# In[19]:


def player():
    count = 1
    while True:
        print('Run count:', count)
        yield from song()
        count += 1


# In[20]:


p = player()


# In[21]:


next(p), next(p)


# In[22]:


next(p), next(p)


# In[23]:


next(p), next(p)


# and so on...
