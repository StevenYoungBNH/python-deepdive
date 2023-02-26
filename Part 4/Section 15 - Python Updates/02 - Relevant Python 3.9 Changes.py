#!/usr/bin/env python
# coding: utf-8

# ### Relevant Python 3.9 Changes

# The release of Python 3.9 has brought some new features.
# 
# This is a summary of the ones _I_ deemed relevant to this course, and does **not** include all the changes!
# 
# For full release details, see [here](https://docs.python.org/3/whatsnew/3.9.html)

# #### Time Zones

# We don't cover 3rd party libraries in this course, but if you've worked with Python in a production environment, you will likely have come across the dreaded timezone and Daylight Savings issues that plague datetimes!

# Most likely you will have resorted to using the `pytz` and `python-dateutil` libraries to help with that.

# Now, Python 3.9 is proud to introduce the `zoneinfo` module to deal with timezones properly. About time too!

# For full info on this, refer to [PEP 615](https://peps.python.org/pep-0615/).
# 
# And the Python [docs](https://docs.python.org/3.9/library/zoneinfo.html#module-zoneinfo).
# 
# **Windows Users**: you will likely need to add a dependency on the `tzdata` [library](https://pypi.org/project/tzdata/) for the IANA time zone database. See [this note](https://docs.python.org/3.9/library/zoneinfo.html#data-sources)
# 
# You should also take a look at this [presentation](https://pganssle-talks.github.io/chipy-nov-2020-zoneinfo/#/) by Paul Ganssle who wrote that module - very interesting read!

# Let's look at how we might have handled timezone and DST using `pytz` and `dateutil`, and contrast that to how we can use the new `zoneinfo` module instead.

# In[1]:


import zoneinfo
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import dateutil
import pytz


# Let's list out all the defined time zones:

# In[2]:


for tz in pytz.all_timezones:
    print(tz)


# With the `zoneinfo` module:

# In[3]:


for tz in sorted(zoneinfo.available_timezones()):
    print(tz)


# Are the time zones defined by `pytz` and `zoneinfo` the same? Yes!

# In this example, let's take our current time in UTC, and convert it to some other time zone, say `Australia/Melbourne`.

# In[4]:


now_utc_naive = datetime.utcnow()


# In[5]:


now_utc_naive


# The problem here is that we have a _naive_ datetime (i.e. one without an attached timezone).

# We can make this naive datetime time zone aware by tacking on the timezone (since we know it is UTC):

# In[6]:


now_utc_aware = now_utc_naive.replace(tzinfo=timezone.utc)
now_utc_aware


# Or, we could use the `pytz` library to do the same thing:

# In[7]:


pytz.utc.localize(datetime.utcnow())


# Now that we have a time zone aware datetime, we can convert it to another timezone using `pytz`:

# First, let's pick a time zone from `pytz`:

# In[8]:


tz_melbourne = pytz.timezone('Australia/Melbourne')


# And now we localize our aware datetime to this time zone:

# In[9]:


now_utc_aware.astimezone(tz_melbourne)


# We could do both these steps in a single expression:

# In[10]:


now_utc_aware.astimezone(pytz.timezone('Australia/Melbourne'))


# Now, let's do the same thing using the `zoneinfo` module.

# Let's pick the same target time zone:

# In[11]:


tz_zi_dublin = ZoneInfo("Europe/Dublin")


# And the let's convert our aware datetime to that time zone:

# In[12]:


now_utc_aware.astimezone(tz_zi_dublin)


# Or, we can also write this as a single expression:

# In[13]:


now_utc_aware.astimezone(ZoneInfo("Europe/Dublin"))


# #### The `math` Module

# Several enhancements or additions have been to the math library.

# The `math` module already had the `gcd` function to calculate the great common divisor of two numbers:

# In[14]:


import math


# In[15]:


math.gcd(27, 45)


# But now `gcd` can take multiple arguments, not just two:

# In[16]:


math.gcd(27, 45, 18, 15)


# The `lcm` (least common multiple) function has been added:

# In[17]:


math.lcm(2, 3, 4)


# #### Dictionary Unions

# When we discussed dictionaries in this course, we saw that we could combine two dictionaries using unpacking:

# In[18]:


d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'c': 30, 'd': 40}


# In[19]:


{**d1, **d2}


# As we saw the second dictionary's key/value pair "overwrote" the key/value pair from the first dictionary.

# We could also use the `ChainMap` function in the `collections` module:

# In[20]:


from collections import ChainMap


# In[21]:


merged = ChainMap(d1, d2)


# In[22]:


merged['a'], merged['c'], merged['d']


# As you can see, in the `ChainMap`, the firest occurrence of the key is used - so in this case `c` comes from `d1`, not `d2`.

# Both of these ways of "combining" dictionaries work well - but they are not very intuitive, and need a little attention to what happens when you have common keys in the dictionaries.

# Think of concatenating lists where we can simply use the `+` operator - this is very intuitive:

# In[23]:


[1, 2, 3] + [4, 5, 6]


# Now dictionaries are not like lists, but they are closely related to **sets**. With sets, we have the **union** operator (`|`):

# In[24]:


s1 = {'a', 'b', 'c'}
s2 = {'c', 'd'}

s1 | s2


# Python 3.9 introduces support for the **union** (`|`) operation between dictionaries as well.

# In[25]:


d1 | d2


# Just like with the `{**d1, **d2}` approach, the value for `c` came from the second dictionary.

# And just like with that technique we can control this by switching the order of the dictionaries in the union:

# In[26]:


d2 | d1


# One question we should have, is what happens to the insertion order that Python dictionaries now guarantee?

# In[27]:


d1 = {'c': 3, 'a': 1, 'b': 2}
d2 = {'d': 40, 'c': 30}


# In[28]:


d1 | d2


# As you can see, even though the **value** for `c` came from the **second** dictionary, the original inertion order of the **keys** is maintained, so `c` is still in first position in the union of the two dictionaries.

# #### String Methods

# Often we need to remove some prefix or suffix in a string.

# For example, we may have this list of string:

# In[29]:


data = [
    "(log) [2022-03-01T13:30:01] Log record 1",
    "(log) [2022-03-01T13:30:02] Log record 2",
    "(log) [2022-03-01T13:30:03] Log record 3",
    "(log) [2022-03-01T13:30:04] Log record 4",
]


# And we want to clean these up and remove the `(log) ` prefix (including the space).

# We can certainly do it this way:

# In[30]:


clean = [
    s.replace("(log) ", '')
    for s in data
]
clean


# You might be tempted to use the `lstrip` method:

# In[31]:


clean = [
    s.lstrip("(log) ")
    for s in data
]
clean


# This appears to work, but `lstrip` (and `rstrip`) does not interpet `"(log )"` as a string, but rather a **sequence** of characters, and each one will be removed - so you might end up with this problem:

# In[32]:


data2 = [
    "(log) log: [2022-03-01T13:30:01] Log record 1",
    "(log) log: [2022-03-01T13:30:02] Log record 2",
    "(log) log: [2022-03-01T13:30:03] Log record 3",
    "(log) log: [2022-03-01T13:30:04] Log record 4",
]


# In[33]:


clean = [
    s.lstrip("(log) ")
    for s in data2
]
clean


# Now that removed a lot more than expected everything from those strings, unlike the replace, which will replace only the first occurrence by default:

# In[34]:


clean = [
    s.replace("(log) ", '')
    for s in data2
]
clean


# Python 3,9 introduces two new string methods to do this without having to use `replace`, namely the `removeprefix()` and `removesuffix()` methods:

# In[35]:


[
    s.removeprefix("(log) ")
    for s in data
]


# In[36]:


[
    s.removeprefix("(log) ")
    for s in data2
]


# Note that if the prefix (or suffix) is not found, nothing happens, the new string will be the same as the original (i.e. no exception is raised):

# In[37]:


'Python rocks!'.removeprefix('Java')

