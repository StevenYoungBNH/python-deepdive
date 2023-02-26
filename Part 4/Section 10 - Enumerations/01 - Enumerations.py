#!/usr/bin/env python
# coding: utf-8

# ### Enumerations

# We'll need the `enum` module:

# In[1]:


import enum


# The base class for enums is `Enum`. To create an enumeration we need to **subclass** it:

# In[2]:


class Color(enum.Enum):
    red = 1
    green = 2
    blue = 3


# Associated values can be anything, not just integer values:

# In[3]:


class Status(enum.Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'    


# In[4]:


class UnitVector(enum.Enum):
    V1D = (1, )
    V2D = (1, 1)
    V3D = (1, 1, 1)


# Each member of an enumeration has a type of the enumeration class itself:

# In[5]:


Status.PENDING


# In[6]:


type(Status.PENDING)


# In[7]:


isinstance(Status.PENDING, Status)


# Each member (instance of the enumeration) has properties, just like any object:

# In[8]:


Status.PENDING.name, Status.PENDING.value


# Although `==` is supported, member equality is generally tested using identity, `is`. It is also faster than using `==`:

# In[9]:


Status.PENDING is Status.PENDING


# In[10]:


Status.PENDING == Status.PENDING


# Note that although `==` (and `!=`) is supported, rich comparison operators are not (it would not make sense, except maybe if the values are values such as integers - we'll come back to that):

# In[11]:


class Constants(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3


# In[12]:


try:
    Constants.ONE > Constants.TWO
except TypeError as ex:
    print(ex)


# Membership can be tested using `in`:

# In[13]:


Status.PENDING in Status


# Note that the names (strings) and associated values are not themselves members of the enumeration - remember that enumeration members are instances of the enumeration class:

# In[14]:


Status.PENDING.name, Status.PENDING.value


# In[15]:


'PENDING' in Status, 'pending' in Status


# Enums are callables, and we can look up a member by **value** by calling the enumeration:

# In[16]:


Status('pending'), UnitVector((1,1))


# But if we try to lookup a member with a non-existent value, we get a `ValueError` exception:

# In[17]:


try:
    Status('invalid')
except ValueError as ex:
    print(ex)


# Recall that a class that implements the `__getitem__` method supports the [] operation:

# In[18]:


class Person:
    def __getitem__(self, val):
        return f'__getitem__({val}) called...'


# In[19]:


p = Person()
p['some value']


# Enumerations implement this `__getitem__` method:

# In[20]:


hasattr(Status, '__getitem__')


# So we can look up a member by it's name (think of it as a key):

# In[21]:


Status['PENDING']


# But the enumeration members, although instances of the enumeration, are also class attributes of the enumeration, so we can also use `getattr` like we would with any standard class attribute:

# In[22]:


getattr(Status, 'PENDING')


# Enumeration members are always hashable, even if their associated values are not (makes sense, since member names are basically strings):

# In[23]:


class Person:
    __hash__ = None


# In[24]:


p = Person()
try:
    hash(p)
except TypeError as ex:
    print(ex)


# So, although `Person` objects are not hashable:

# In[25]:


class Family(enum.Enum):
    person_1 = Person()
    person_2 = Person()


# In[26]:


Family.person_1


# We can still use members as keys in a dictionary:

# In[27]:


{
    Family.person_1: 'person 1',
    Family.person_2: 'person 2'
}


# Enumerations are iterables:

# In[28]:


hasattr(Status, '__iter__')


# So we can iterate over the members:

# In[29]:


for member in Status:
    print(repr(member))


# Note that iteration order is the order in which the members are declared in the enumeration, and has nothing to do with the associated values:

# In[30]:


class Numbers1(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    
class Numbers2(enum.Enum):
    THREE = 3
    TWO = 2
    ONE = 1


# In[31]:


list(Numbers1)


# In[32]:


list(Numbers2)


# Lastly, enumerations are immutable: we cannot add/remove elements from the enumeration, **and** we canniot modify the associated values:

# In[33]:


try:
    Status.PENDING.value = 10
except AttributeError as ex:
    print(ex)


# In[34]:


try:
    Status['NEW'] = 100
except TypeError as ex:
    print(ex)


# We'll come back to this later, but we cannot extend an enumeration once it has members defined:

# In[35]:


class EnumBase(enum.Enum):
    pass


# In[36]:


class EnumExt(EnumBase):
    ONE = 1
    TWO = 2


# In[37]:


EnumExt.ONE


# But this would not work:

# In[38]:


class EnumBase(enum.Enum):
    ONE = 1


# In[39]:


try:
    class EnumExt(EnumBase):
        TWO = 2
except TypeError as ex:
    print(ex)


# ##### Example

# So the basics of enumerations are quite straightforward. You might be wondering though why we have two ways of referencing members by name:

# In[40]:


Status.PENDING, Status['PENDING']


# This is because sometimes we might get a string from some input, and need to match it up with a member in the enumeration.

# For example it might be a status that comes back from an API call in a JSON payload:

# In[41]:


payload = """
{
  "name": "Alex",
  "status": "PENDING"
}
"""


# In[42]:


import json

data = json.loads(payload)


# In[43]:


data['status']


# And now we can look up the status in the enumeration, but we have to use the `__getitem__` method:

# In[44]:


Status[data['status']]


# ##### Example 2

# A natural question given the last example might be: how do we determine if some string corresponds to a member name in our enumeration?

# We have three basic ways of doing this.

# First we could simply lookup the value by name, and trap the `KeyError` exception:

# In[45]:


def is_member(en, name):
    try:
        en[name]
    except KeyError:
        return False
    return True


# In[46]:


is_member(Status, 'PENDING')


# In[47]:


is_member(Status, 'pending')


# We could also just use the `getattr` function:

# In[48]:


getattr(Status, 'PENDING', None), getattr(Status, 'OK', None)


# But we could also just use the `__members__` property:

# In[49]:


Status.__members__


# As you can see we get a `mappingproxy` object back, so we can use membership in that object (that defaults to using the keys), or the `keys()` view if we want to be more explicit:

# In[50]:


'PENDING' in Status.__members__


# In[51]:


'PENDING' in Status.__members__.keys()


# In[ ]:




