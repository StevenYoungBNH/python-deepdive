#!/usr/bin/env python
# coding: utf-8

# ### Relevant Python 3.8 Changes

# The release of Python 3.8 has brought some new features.
# 
# This is a summary of the ones _I_ deemed relevant to this course, and does **not** include all the changes!
# 
# For full release details, see [here](https://docs.python.org/3/whatsnew/3.8.html)

# #### Positional Only Parameters

# It is now possible to define **positional-only** parameters for Python functions.

# As we saw earlier in this course, when you define positional parameters in a function:

# In[1]:


def my_func(a, b):
    return a + b


# the user is free to pass arguments either positionally:

# In[2]:


my_func(1, 2)


# or, as named arguments:

# In[3]:


my_func(b=2, a=1)


# Some functions in Python's built-ins ared defined in such a way that certain parameters can **only** be passed positionally, for example the `print` function:

# In[4]:


help(print)


# That `value` cannot be passed by name:

# In[5]:


try:
    print(value="hello")
except TypeError as ex:
    print(ex)


# Instead, the parameter **must** be passed positionally:

# In[6]:


print("hello")


# Until Python 3.8, it was not possible to reproduce such behavior with user-defined functions.

# Now you can, by using the slash character(`/`). Parameters defined **before** the `/` become **positional-only** parameters:

# In[7]:


def my_func(a, b, /):
    return a + b


# In[8]:


my_func(1, 2)


# In[9]:


try:
    my_func(a=1, b=2)
except TypeError as ex:
    print(ex)


# You can of course mix this along with the special parameters `*` and `**`:

# In[10]:


def my_func(a, b, /, *, c):
    print(a + b + c)


# In[11]:


my_func(1, 2, c=10)


# #### f-string Enhancements

# Often we use f-strings to interpolate the name of a variable and it's value:

# In[12]:


a, b = "hello", "world"
print(f"a={a}, b={b}")


# Python 3.8 provides a shortcut way of doing the same thing:

# In[13]:


print(f"{a=}, {b=}")


# You can even use [format specifiers](https://docs.python.org/3/library/string.html#formatspec)
# to further customize the output:

# In[14]:


print(f"{a=:s}, {b=:s}")


# Or when dealing with other types:

# In[15]:


from datetime import datetime
from math import pi


# In[16]:


d = datetime.utcnow()
e = pi


# In[17]:


print(f"{d=}, {e=}")


# And applying some format specifiers:

# In[18]:


print(f"{d=:%Y-%m-%d %H:%M:%S}, {e=:.3f}")


# It will even display the text of an expression if you use one in your f-string:

# In[19]:


sentence = ["Python", "rocks!"]
print(f"{1 + 2=}, {' '.join(sentence)=}")


# #### The `as_integer_ratio()` Method

# The types `bool`, `int` and `Fraction` now all implement an `as_integer_ratio()` method which returns a tuple consisting of the numerator and denominator. Remember that `Decimal` and `float` already implement the same method.

# In[20]:


from fractions import Fraction


# In[21]:


f = Fraction(2, 3)


# In[22]:


f.as_integer_ratio()


# In[23]:


a = 12
a.as_integer_ratio()


# In[24]:


flag = True
flag.as_integer_ratio()


# The advantage of this is mainly for polymorphism (or duck-typing), where you can now use `as_integer_ratio` irrespective of whether the variable is a `bool`, an `int`, a `float`, a `Decimal` or a `Fraction`.

# In[25]:


from decimal import Decimal


# In[26]:


Decimal("0.33").as_integer_ratio()


# In[27]:


(3.14).as_integer_ratio()


# #### The `lru_cache` decorator

# As we saw in this course, we can use the `lru_cache` decorator to appky an LRU cache to our functions:

# In[28]:


from functools import lru_cache


# In[29]:


@lru_cache(maxsize=3)
def fib(n):
    if n <=2 :
        return 1
    else:
        return fib(n-1) + fib(n-2)


# In[30]:


fib(100)


# If we don't specify `maxsize`, it will default to `128`:

# In[31]:


@lru_cache()
def fib(n):
    if n <=2 :
        return 1
    else:
        return fib(n-1) + fib(n-2)


# In[32]:


fib(100)


# The change made to this decorator in Python 3.8 allows us not to use those empty parentheses:

# In[33]:


@lru_cache
def fib(n):
    if n <=2 :
        return 1
    else:
        return fib(n-1) + fib(n-2)


# #### `math` Module

# Many examples I use throughout this course calculate the Euclidean distance between two points:

# In[34]:


import math


# In[35]:


a = (0, 0)
b = (1, 1)

dist = math.sqrt((b[0] - a[1]) ** 2 + (b[1] - a[1]) ** 2)
print(dist)


# Now, it's much easier using the `dist()` function the `math` module:

# In[36]:


math.dist(a, b)


# #### The `namedtuple` Implementation

# Actually these changes were added to Python 3.7, but since I don't have a separate lecture for Python 3.7 changes (most did not apply to this course), here it is.

# The `_source` attribute was **removed**. There quite a discussion on this, and the the core dev who implemented and supported this essentially gave up trying to keep this in - it was deemed to cause too much "overhead". So, sadly (wearing my teacher's hat), it is gone. It is no more. It's not pining, it's just dead. :-)

# The method I showed you for defining defaults for named tuples still works, and could still be used, but Python 3.7 added the `defaults` parameter to the named tuple definition.

# In[37]:


from collections import namedtuple


# In[38]:


NT = namedtuple("NT", "a b c", defaults=(10, 20, 30))


# In[39]:


nt = NT()


# In[40]:


nt


# You don't have to specify defaults for everything, but if you do not, be aware that defaults will be applied from **right** to **left**. Which makes sense given that in Python non-defaulted parameters must be defined **before** defaulted parameters.

# In[41]:


NT = namedtuple("NT", "a b c", defaults = (20, 30))


# In[42]:


nt = NT(10)


# In[43]:


nt


# Note that with this way of specifying defaults you can easily define the same default for all items in the named tuple using the `*` operator:

# In[44]:


NT = namedtuple("NT", "a b c d e f", defaults=("xyz",) * 6)


# In[45]:


nt = NT()


# In[46]:


nt


# Just be careful if you use a **mutable** type to do this!!

# In[47]:


NT = namedtuple("NT", "a b c", defaults = ([],) * 3)


# In[48]:


nt = NT()


# In[49]:


nt


# In[50]:


nt.a.append(10)


# In[51]:


nt.a


# But watch this!

# In[52]:


nt


# I hope you understand what happened here without me telling you!

# The **same** list object was re-used 3 times in the defaults.

# You can easily recover your defaults using the `_field_defaults` method:

# In[53]:


NT = namedtuple("NT", "a, b, c", defaults=(1, 2, 3))


# In[54]:


NT._field_defaults


# One change of note in Python 3.8, the `_as_dict()` method now returns a standard dictionary (key ordered in the same way as the named tuple). Prior to this version, it would return an `OrderedDict` since standard Python dictionaries did not guarantee any specific key order, but since they now do, there's no need to use the `DefaultDict` anymore.

# #### Other Things

# These are few other odds and ends that you might find of interest:

# The built-in `reversed` function now works with dictionary views:

# In[55]:


d = {'a': 1, 'b': 2}


# In[56]:


list(d.keys())


# In[57]:


list(reversed(d.keys()))


# In[58]:


list(reversed(d.values()))


# In[59]:


list(reversed(d.items()))


# The `continue` statement was not permitted in the `finally` clause of a loop, but is now supported.

# Earlier in Part 1, we discussed string interning, as well as how a small selection of integers are essentially "cached" by Python and re-used whenever the literal is encountered. This meant we could use `is` instead of `==` in some cases, and that helped us get a clearer understanding of what's going on. **BUT**, as we also discussed, you should **not**, in practice, use `is` for comparing objects such as integers, strings, etc (usually we are more interested in whether is the same value, rather than the identical object) - the fact that this works is an implementation detail and not guaranteed to work the same way from one Python version to another.
# 
# Although linters will usually catch those kinds of issues, not everyone uses a Python linter - so Python 3.8 will now emit a **warning** if you compare variables of certain types with literal constants!

# In[60]:


a = 1
a is 1


# In[61]:


a = 'hello'
a is 'hello'


# But we do not get a warning in a situation such as this:

# In[62]:


a = [1, 2, 3]

a is [1, 2, 3]

