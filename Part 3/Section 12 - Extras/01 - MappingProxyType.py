#!/usr/bin/env python
# coding: utf-8

# ### MappingProxyType

# The mapping proxy type is an easy way to create a read-only **view** of any dictionary.
# 
# This can be handy if you want to pass a dictionary around, and have that view reflect the underlying dictionary (even if it is mutated), but not allow the receiver to be able to modify the dictionary.

# In fact, this is used by classes all the time:

# In[1]:


class Test:
    a = 100


# In[2]:


Test.__dict__


# As you can see, what is returned here is not actually a `dict` object, but a `mappingproxy`.

# To create a mapping proxy from a dictionary we use the `MappingProxyType` from the `types` module:

# In[3]:


from types import MappingProxyType


# In[4]:


d = {'a': 1, 'b': 2}


# In[5]:


mp = MappingProxyType(d)


# This mapping proxy still behaves like a dictionary:

# In[6]:


list(mp.keys())


# In[7]:


list(mp.values())


# In[8]:


list(mp.items())


# In[9]:


mp.get('a', 'not found')


# In[10]:


mp.get('c', 'not found')


# But we cannot mutate it:

# In[11]:


try:
    mp['a'] = 100
except TypeError as ex:
    print('TypeError: ', ex)


# On the other hand, if the underlying dictionary is mutated:

# In[12]:


d['a'] = 100
d['c'] = 'new item'


# In[13]:


d


# In[14]:


mp


# And as you can see, the mapping proxy "sees" the changes in the undelying dictionary - so it behaves like a view, in the same way `keys()`, `values()` and `items()` do.

# You can obtain a **shallow** copy of the proxy by using the `copy()` method:

# In[15]:


cp = mp.copy()


# In[16]:


cp


# As you can see, `cp` is a plain `dict`.

# In[ ]:




