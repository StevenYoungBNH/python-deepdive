#!/usr/bin/env python
# coding: utf-8

# ### Hashing and Equality

# By default, when we create a custom class, we inherit `__eq__` and `__hash__` from the `object` class.

# In[1]:


dir(object)


# This means that by default our custom classes produce hashable objects that can be used in mapping types such as dictionaries and sets.

# In[2]:


class Person:
    pass


# In[3]:


p1 = Person()
p2 = Person()


# In[4]:


hash(p1), hash(p2)


# In[5]:


p1 == p2


# By default `__hash__` uses the object's identity, and `__eq__` will only evaluate to `True` if the two objects are the same objects (identity).

# We can override those default implementations ourselves. 

# If we override the `__eq__` method, Python will automatically make our class unhashable:

# In[6]:


class Person:
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        return isinstance(other, Person) and self.name == other.name
            


# In[7]:


p1 = Person('John')
p2 = Person('John')
p3 = Person('Eric')


# In[8]:


p1 == p2, p1 == p3


# But now we have lost hashing:

# In[9]:


try:
    hash(p1)
except TypeError as ex:
    print(ex)


# This is because two objects that compare equal should also have the same hash. However, Python's default is to use the object's identity. So if that were the case then `p1` and `p2` would be equal, but would not have the same hash.
# 
# So Python sets the `__hash__` property to `None`:

# In[10]:


type(p1.__hash__)


# The downside to this is that we can no longer use instances of this class as keys in a dictionary or elements of a set:

# In[11]:


try:
    d = {p1: 'person 1'}
except TypeError as ex:
    print(ex)


# We can however provide our own override for `__hash__`:

# In[12]:


class Person:
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        return isinstance(other, Person) and self.name == other.name
            
    def __hash__(self):
        return hash(self.name)


# We now have a `Person` class that supports equality based on the state of the class (the `name` in this instance) and is hashable too.
# 
# We should also keep in mind that for this to work well in data structurfes such as dictionaries, what we use to create a hash of the class should remain immutable.
# 
# So, a better approach would be to make the `name` property a read-only property:

# In[13]:


class Person:
    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name
    
    def __eq__(self, other):
        return isinstance(other, Person) and self.name == other.name
            
    def __hash__(self):
        return hash(self.name)


# And now our Person instances can be used in sets and dictionaries (keys)

# In[14]:


p1 = Person('Eric')


# In[15]:


d = {p1: 'Eric'}


# In[16]:


d


# In[17]:


s = {p1}


# And of course since we now have equality defined in terms of the object state (and not the default of, essentially, the memory address), we can recover an element from a dictionary using different objects (identity wise) that have the same state (equality wise).
