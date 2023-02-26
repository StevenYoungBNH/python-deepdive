#!/usr/bin/env python
# coding: utf-8

# ### Using decorators to prime coroutines

# We saw how we always to 'prime' a coroutine (i.e. get the generator in a suspended state) before we can start sending values to it.
# 
# This is something that **must** always be done - and this is an excellent use case for decorators.
# 
# We're going to create a decorator that will create and prime the coroutine for us.
# 
# Essentially we want to be able to:
# 1. create the coroutine (`gen()`)
# 2. prime the coroutine (`next(g)`)
# 
# in one step - so that's what the decorator is going to do - it will wrap our original coroutine and return a new function that will perform those steps for us, and return the newly created and primed coroutine:

# In[31]:


def coroutine(gen_fn):
    def inner():
        gen = gen_fn()
        next(gen)
        return gen
    return inner    


# In[32]:


@coroutine
def echo():
    while True:
        received = yield
        print(received)


# In[33]:


ec = echo()


# In[34]:


import inspect
inspect.getgeneratorstate(ec)


# As you can see our generator was automatically advanced from CREATED to SUSPENDED - and we can now use it straight away:

# In[36]:


ec.send('hello')


# Now, we still need to expand this slightly to accomodate passing arguments to our generator function (coroutine):

# In[65]:


def coroutine(gen_fn):
    def inner(*args, **kwargs):
        gen = gen_fn(*args, **kwargs)
        next(gen)
        return gen
    return inner  


# In[66]:


import math

@coroutine
def power_up(p):
    result = None
    while True:
        received = yield result
        result = math.pow(received, p)       


# In[67]:


squares = power_up(2)
cubes = power_up(3)


# In[68]:


squares.send(2)


# In[69]:


cubes.send(2)


# What happens if we send the wrong type in?

# In[70]:


squares.send('abc')


# And now our generator stops functioning, it is in a closed state:

# In[71]:


inspect.getgeneratorstate(squares)


# In this particular case, we don't want our generator to close down - it should simply yield None and ignore the exception, so it can continue working:

# In[72]:


@coroutine
def power_up(p):
    result = None
    while True:
        received = yield result
        try:
            result = math.pow(received, p)    
        except TypeError:
            result = None


# In[73]:


squares = power_up(2)


# In[74]:


squares.send(2)


# In[75]:


squares.send('abc')


# In[76]:


squares.send(3)


# Of course, we can close the generator ourselves still:

# In[77]:


squares.close()


# In[78]:


inspect.getgeneratorstate(squares)


# In[ ]:




