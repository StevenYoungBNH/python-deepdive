#!/usr/bin/env python
# coding: utf-8

# ### Yield From - Closing and Return

# Just as we can send `next` and `send` through a delegator, we can also send `close`.
# 
# How does this affect the delegator and the subgenerator?
# 
# Let's take a look.

# In[1]:


def subgen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('subgen: closing...')


# In[2]:


def delegator():
    s = subgen()
    yield from s
    yield 'delegator: subgen closed'
    print('delegator: closing...')


# In[3]:


d = delegator()
next(d)


# At this point, both the delegator and the subgenerator are primed and suspended:

# In[4]:


from inspect import getgeneratorstate, getgeneratorlocals


# In[5]:


getgeneratorlocals(d)


# In[6]:


s = getgeneratorlocals(d)['s']
print(getgeneratorstate(d))
print(getgeneratorstate(s))


# We can send data to the delegator:

# In[7]:


d.send('hello')


# We can even send data directly to the subgenerator since we now have a handle on it:

# In[8]:


s.send('python')


# In fact, we can close it too:

# In[9]:


s.close()


# So, what is the state of the delegator now?

# In[10]:


getgeneratorstate(d)


# But the subgenerator closed, so let's see what happens when we call `next` on `d`:

# In[11]:


next(d)


# As you can see, the generator code resume right after the `yield from`, and we can do this one more time to close the delegator:

# In[12]:


next(d)


# OK, so this is what happens when the subgenerator closes (directly or indirectly) - the delegator simply resumes running right after the `yield from` when we call `next`.
# 
# But what happens if we close the delegator instead of just closing the subgenerator?

# In[13]:


d = delegator()
next(d)
s = getgeneratorlocals(d)['s']
print(getgeneratorstate(d))
print(getgeneratorstate(s))


# In[14]:


d.close()


# As you can see the subgenerator also closed. Is the delegator closed too?

# In[15]:


print(getgeneratorstate(d))
print(getgeneratorstate(s))


# Yes. So closing the delegator will close not only the delegator itself, but also close the currently active subgenerator (if any).

# We should notice that when we closed the subgenerator directly no apparent exception was raised in our context.
# 
# What happens if the subgenerator returns something when it closes?

# In[16]:


def subgen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('subgen: closing...')
        return 'subgen: return value'


# In[17]:


s = subgen()
next(s)
s.send('hello')
s.close()


# Hmmm, the `StopIteration` exception was silenced. Let's do this a different way, since we know the `StopIteration` exception should contain the return value:

# In[18]:


s = subgen()
next(s)
s.send('hello')
s.throw(GeneratorExit, 'force exit')


# OK, so now we can see that the `StopIteration` exception contains the return value.
# 
# The `yield from` actually captures that value as it's return value - in other words `yield from` is not just a statement, it is in fact, like `yield`, also an expression.
# 
# Let's see how that works:

# In[19]:


def subgen():
    try:
        yield 1
        yield 2
    finally:
        print('subgen: closing...')
        return 100


# In[20]:


def delegator():
    s = subgen()
    result = yield from s
    print('subgen returned:', result)
    yield 'delegator suspended'
    print('delegator closing')


# In[21]:


d = delegator()


# In[22]:


next(d)


# In[23]:


next(d)


# In[24]:


next(d)


# As you can see the return value of the subgenerator ended up as the result of the `yield from` expression. 
