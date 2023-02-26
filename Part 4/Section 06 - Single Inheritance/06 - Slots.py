#!/usr/bin/env python
# coding: utf-8

# ### Slots

# Let's start with an example of how we use slots:

# In[1]:


class Location:
    __slots__ = 'name', '_longitude', '_latitude'
    
    def __init__(self, name, longitude, latitude):
        self._longitude = longitude
        self._latitude = latitude
        self.name = name
        
    @property
    def longitude(self):
        return self._longitude
    
    @property
    def latitude(self):
        return self._latitude


# `Location` still has that mapping proxy, and we can still add and remove **class** attributes from `Location`:

# In[2]:


Location.__dict__


# In[3]:


Location.map_service = 'Google Maps'


# In[4]:


Location.__dict__


# But the use of `slots` affects **instances** of the class:

# In[5]:


l = Location('Mumbai', 19.0760, 72.8777)


# In[6]:


l.name, l.longitude, l.latitude


# The **instance** no longer has a dictionary for maintaining state:

# In[7]:


try:
    l.__dict__
except AttributeError as ex:
    print(ex)


# This means we can no longer add attributes to the instance:

# In[8]:


try:
    l.map_link = 'http://maps.google.com/...'
except AttributeError as ex:
    print(ex)


# Now we can actually delete the attribute from the instance:

# In[9]:


del l.name


# And as we can see the instance now longer has that attribute:

# In[10]:


try:
    print(l.name)
except AttributeError as ex:
    print(f'Attribute Error: {ex}')


# However we can still re-assign a value to that same attribute:

# In[11]:


l.name = 'Mumbai'


# In[12]:


l.name


# Mainly we use slots when we expect to have many instances of a class and to gain a performance boost (mostly storage, but also attribute lookup speed). 

# In[ ]:




