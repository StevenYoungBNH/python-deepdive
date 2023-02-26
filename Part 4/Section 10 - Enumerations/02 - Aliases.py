#!/usr/bin/env python
# coding: utf-8

# ### Aliases

# Although member values are considered unique in enumerations, we can still define multiple member names with the same value. But they do not create different members!
# 

# They are, in fact, considered aliases of each other, with the first member becoming the "master" member.

# Let's see a simple example of this first:

# In[1]:


import enum


# In[2]:


class NumSides(enum.Enum):
    Triangle = 3
    Rectangle = 4
    Square = 4
    Rhombus = 4


# As you can see we have two members with different names (names must **always** be unique), but with the **same** value.

# However, the `Square` and `Rhombus` members are considered **aliases** of the `Rectangle` member since `Rectangle` is defined first.

# This means that `Rectangle` and `Square` are actually considered the **same** member:

# In[3]:


NumSides.Rectangle is NumSides.Square


# And of course aliases are equal to each other too:

# In[4]:


NumSides.Square is NumSides.Rhombus


# Aliases can be referenced just like an ordinary member, and are considered *contained* in the enumeration:

# In[5]:


NumSides.Square in NumSides


# And when we look up the member, by value:

# In[6]:


NumSides(4)


# we always get the "master" back.

# Same holds when when looking up by key:

# In[7]:


NumSides['Square']


# When we iterate an enumeration that contains aliases, none of the aliases are returned in the iteration:

# In[8]:


list(NumSides)


# The only way to get all the members, including aliases, is to use the `__members__` property:

# In[9]:


NumSides.__members__


# Notice how the aliases are treated. Although the keys in the mapping proxy are different, the object they point to are all the "master" member.

# #### Example

# There are times when the ability to define these aliases can be useful. Let's say you have to deal with statuses that are returned as strings from different systems.

# These systems may not always define exactly the same strings to mean the same thing (maybe they were developed independently). In a case like this, being able to create aliases could be useful to bring uniformity to our own code.

# Let's say that the statuses from system 1 are: `ready, busy, finished_no_error, finished_with_errors`

# And for system 2 we have correspondingly: `ready, processing, ran_ok, errored`

# And in our own system we might want the statuses: `ready, running, ok, errors`

# In other words we have:
# 
# ```
# Us        System 1               System 2
# -------------------------------------------
# ready     ready                  ready
# running   busy                   processing
# ok        finished_no_error      ran_ok
# errors    finished_with_errors   errored
# ```

# We can the easily achieve this using this class with aliases:

# In[10]:


class Status(enum.Enum):
    ready = 'ready'
    
    running = 'running'
    busy = 'running'
    processing = 'running'
    
    ok = 'ok'
    finished_no_error = 'ok'
    ran_ok = 'ok'
    
    errors = 'errors'
    finished_with_errors = 'errors'
    errored = 'errors'


# Then when we list our own statuses, we only see our (master) members:

# In[11]:


list(Status)


# But now we can look up a status from any of the other two systems, and automatically get our "master" member:

# In[12]:


Status['busy']


# In[13]:


Status['processing']


# Note that in our case the actual value of the members does not matter. I used strings, but we could equally well just use numbers:

# In[14]:


class Status(enum.Enum):
    ready = 1
    
    running = 2
    busy = 2
    processing = 2
    
    ok = 3
    finished_no_error = 3
    ran_ok = 3
    
    errors = 4
    finished_with_errors = 4
    errored = 4


# This will work the same way:

# In[15]:


Status.ran_ok


# In[16]:


status = 'ran_ok'


# In[17]:


status in Status.__members__


# In[18]:


Status[status]


# #### Ensuring No Aliases

# Sometimes we want to make sure we are creating enumerations that do **not** contain aliases.

# Of course, we can just be careful and not define aliases, but the `enum` module provides a special decorator that can enforce this:

# In[19]:


@enum.unique
class Status(enum.Enum):
    ready = 1
    done_ok = 2
    errors = 3


# And if we try to create aliases, our code will not compile - we'll get an exception as soon as the class is compiled:

# In[20]:


try:
    @enum.unique
    class Status(enum.Enum):
        ready = 1
        waiting = 1
        done_ok = 2
        errors = 3
except ValueError as ex:
    print(ex)


# So if you know that your enumeration should never contain aliases, go ahead and use the decorator for extra safety.

# In[ ]:




