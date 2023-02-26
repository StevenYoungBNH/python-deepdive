#!/usr/bin/env python
# coding: utf-8

# ### Creating Python Dictionaries

# There are different mechanisms available to create dictionaries in Python.

# #### Literals

# We can use a literal to create a dictionary:

# In[1]:


a = {'k1': 100, 'k2': 200}


# In[2]:


a


# Note that the order in which the items are listed in the literal is maintained when listing out the elements of the dictionary. This does not hold for Python version earlier than 3.6 (practically, version 3.5).

# Another thing to note is that dictionary **keys** must be hashable objects. Associated values on the other hand can be any object.

# So tuples of hashable objects are themselves hashable, but lists are not, even if they only contain hashable elements. Tuples of non-hashable elements are also not hashable.

# In[3]:


hash((1, 2, 3))


# In[4]:


hash([1, 2, 3])


# In[5]:


hash(([1, 2], [3, 4]))


# So we can create dictionaries that look like this:

# In[6]:


a = {('a', 100): ['a', 'b', 'c'], 'key2': {'a': 100, 'b': 200}}


# In[7]:


a


# Interestingly, functions are hashable:

# In[8]:


def my_func(a, b, c):
    print(a, b, c)


# In[9]:


hash(my_func)


# Which means we can use functions as keys in dictionaries:

# In[10]:


d = {my_func: [10, 20, 30]}


# A simple application of this might be to store the argument values we want to use to call the function at a later time:

# In[11]:


def fn_add(a, b):
    return a + b

def fn_inv(a):
    return 1/a

def fn_mult(a, b):
    return a * b


# In[12]:


funcs = {fn_add: (10, 20), fn_inv: (2,), fn_mult: (2, 8)}


# Remember that when we iterate through a dictionary we are actually iterating through the keys:

# In[13]:


for f in funcs:
    print(f)


# We can then call the functions this way:

# In[14]:


for f in funcs:
    result = f(*funcs[f])
    print(result)


# We can also iterate through the items (as tuples) in a dictionary as follows:

# In[15]:


for f, args in funcs.items():
    print(f, args)


# So we could now call each function this way:

# In[16]:


for f, args in funcs.items():
    result = f(*args)
    print(result)


# #### Using the class constructor

# We can also use the class constructor `dict()` in different ways:

# ##### Keyword Arguments

# In[17]:


d = dict(a=100, b=200)


# In[18]:


d


# The restriction here is that the key names must be valid Python identifiers, since they are being used as argument names.

# We can also build a dictionary by passing it an iterable containing the keys and the values:

# In[19]:


d = dict([('a', 100), ('b', 200)])


# In[20]:


d


# The restriction here is that the elements of the iterable must themselves be iterables with exactly two elements.

# In[21]:


d = dict([('a', 100), ['b', 200]])


# In[22]:


d


# Of course we can also pass a dictionary as well:

# In[23]:


d = {'a': 100, 'b': 200, 'c': {'d': 1, 'e': 2}}


# Here I am using a dictionary that happens to contain a nested dictionary for the key `c`.

# Let's look at the id of `d`:

# In[24]:


id(d)


# And let's create a dictionary:

# In[25]:


new_dict = dict(d)


# In[26]:


new_dict


# What's the id of `new_dict`?

# In[27]:


id(new_dict)


# As you can see, we have a new object - however, what about the nested dictionary?

# In[28]:


id(d['c']), id(new_dict['c'])


# As you can see they are the same - so be careful, using the `dict` constructor this way essentially creates a **shallow copy**.
# 
# We'll come back to copying dicts later.

# #### Using Comprehensions

# We can also create dictionaries using a dictionary comprehension.
# This is very similar to list comprehensions or generator expressions.

# Suppose we have two iterables, one containing some keys, and one containing some values we want to associate with each key:

# In[29]:


keys = ['a', 'b', 'c']
values = (1, 2, 3)


# We can then easily create a dictionary this way - the non-Pythonic way!

# In[30]:


d = {}  # creates an empty dictionary
for k, v in zip(keys, values):
    d[k] = v


# In[31]:


d


# But it is much simpler to use a dictionary comprehension:

# In[32]:


d = {k: v for k, v in zip(keys, values)}


# In[33]:


d


# Dictionary comprehensions support the same syntax as list comprehensions - you can have nested loops, `if` statements, etc.

# In[34]:


keys = ['a', 'b', 'c', 'd']
values = (1, 2, 3, 4)

d = {k: v for k, v in zip(keys, values) if v % 2 == 0}


# In[35]:


d


# In the following example we are going to create a grid of 2D coordinate pairs, and calculate their distance from the origin:

# In[36]:


x_coords = (-2, -1, 0, 1, 2)
y_coords = (-2, -1, 0, 1, 2)


# If you remember list comprehensions, we would create all possible `(x,y)` pairs using nested loops (a Cartesian product):

# In[37]:


grid = [(x, y) 
         for x in x_coords 
         for y in y_coords]
grid


# In[38]:


import math


# We can use the `math` module's `hypot` function to do calculate these distances

# In[39]:


math.hypot(1, 1)


# So to calculate these distances for all our points we would do this:

# In[40]:


grid_extended = [(x, y, math.hypot(x, y)) for x, y in grid]
grid_extended


# We can now easily tweak this to make a dictionary, where the coordinate pairs are the key, and the distance the value:

# In[41]:


grid_extended = {(x, y): math.hypot(x, y) for x, y in grid}


# In[42]:


grid_extended


# #### Using `fromkeys`

# The `dict` class also provides the `fromkeys` method that we can use to create dictionaries.
# This class method is used to create a dictionary from an iterable containing the keys, and a **single** value used to assign to each key.

# In[43]:


counters = dict.fromkeys(['a', 'b', 'c'], 0)


# In[44]:


counters


# If we do not specify a value, then `None` is used:

# In[45]:


d = dict.fromkeys('abc')


# In[46]:


d


# Notice how I used the fact that strings are iterables to specify the three single character keys for this dictionary!

# `fromkeys` method will insert the keys in the order in which they are retrieved from the iterable:

# In[47]:


d = dict.fromkeys('python')


# In[48]:


d


# Uh-Oh!! Looks like the ordering didn't work!!
# I've pointed this out a few times already, but Jupyter (this notebook), uses a printing mechanism that will order the keys alphabetically.
# 
# To see the real order of the keys in the dict we should use the print statement ourselves:

# In[49]:


print(d)


# Much better! :-)
