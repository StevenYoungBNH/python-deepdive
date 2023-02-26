#!/usr/bin/env python
# coding: utf-8

# ### Decorators (Part 1)

# Recall the example in the last section where we wrote a simple closure to count how many times a function had been run:

# In[1]:


def counter(fn):
    count = 0
    
    def inner(*args, **kwargs):
        nonlocal count
        count += 1
        print('Function {0} was called {1} times'.format(fn.__name__, count))
        return fn(*args, **kwargs)
    return inner


# In[2]:


def add(a, b=0):
    """
    returns the sum of a and b
    """
    return a + b


# In[3]:


help(add)


# Here's the memory address that `add` points to:

# In[4]:


id(add)


# Now we create a closure using the `add` function as an argument to the `counter` function:

# In[5]:


add = counter(add)


# And you'll note that `add` is no longer the same function as before. Indeed the memory address `add` points to is no longer the same:

# In[6]:


id(add)


# In[7]:


add(1, 2)


# In[8]:


add(2, 2)


# What happened is that we put our **add** function 'through' the **counter** function - we usually say that we **decorated** our function **add**.
# 
# And we call that **counter** function a **decorator**.
# 
# There is a shorthand way of decorating our function without having to type:
# 
# ``func = counter(func)``

# In[9]:


@counter
def mult(a: float, b: float=1, c: float=1) -> float:
    """
    returns the product of a, b, and c
    """
    return a * b * c


# In[10]:


mult(1, 2, 3)


# In[11]:


mult(2, 2, 2)


# Let's do a little bit of introspection on our two decorated functions:

# In[12]:


add.__name__


# In[13]:


mult.__name__


# As you can see, the name of the function is no longer **add** or **mult**, but instead it is the name of that **inner** function in our decorator.

# In[14]:


help(add)


# In[15]:


help(mult)


# As you can see, we've also lost our docstring and parameter annotations!

# What about introspecting the parameters of **add** and **mult**:

# In[16]:


import inspect


# In[17]:


inspect.getsource(add)


# In[18]:


inspect.getsource(mult)


# Even the signature is gone:

# In[19]:


inspect.signature(add)


# In[20]:


inspect.signature(mult)


# Even the parameter defaults documentation is are gone:

# In[21]:


inspect.signature(add).parameters


# In general, when we create decorated functions, we end up "losing" a lot of the metadata of our original function!

# However, we **can** put that information back in - it can get quite complicated.
# 
# Let's see how we might be able to do that for some simple things, like the docstring and the function name.

# In[22]:


def counter(fn):
    count = 0
    
    def inner(*args, **kwargs):
        nonlocal count
        count += 1
        print("{0} was called {1} times".format(fn.__name__, count))
    inner.__name__ = fn.__name__
    inner.__doc__ = fn.__doc__
    return inner


# In[23]:


@counter
def add(a: int, b: int=10) -> int:
    """
    returns sum of two integers
    """
    return a + b


# In[24]:


help(add)


# In[25]:


add.__name__


# At least we have the docstring and function name back... But what about the parameters? Our real **add** function takes two positional parameters, but because the closure used a generic way of accepting **\*args** and **\*\*kwargs**, we lose this information

# We can use a special function in the **functools** module, called **wraps**. In fact, that function is a decorator itself!

# In[26]:


from functools import wraps


# In[27]:


def counter(fn):
    count = 0
    
    @wraps(fn)
    def inner(*args, **kwargs):
        nonlocal count
        count += 1
        print("{0} was called {1} times".format(fn.__name__, count))

    return inner


# In[28]:


@counter
def add(a: int, b: int=10) -> int:
    """
    returns sum of two integers
    """
    return a + b


# In[29]:


help(add)


# Yay!!! Everything is back to normal.

# In[30]:


inspect.getsource(add)


# In[31]:


inspect.signature(add)


# In[32]:


inspect.signature(add).parameters

