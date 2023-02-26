#!/usr/bin/env python
# coding: utf-8

# ### Booleans: Precedence and Short-Circuiting

# In[1]:


True or True and False


# this is equivalent, because of ``and`` having higer precedence than ``or``, to:

# In[3]:


True or (True and False)


# This is not the same as:

# In[2]:


(True or True) and False


# #### Short-Circuiting

# In[13]:


a = 10
b = 2

if a/b > 2:
    print('a is at least double b')


# In[12]:


a = 10
b = 0

if a/b > 2:
    print('a is at least double b')


# In[11]:


a = 10
b = 0

if b and a/b > 2:
    print('a is at least double b')


# Can also be useful to deal with null or empty strings in a database:

# In[14]:


import string


# In[15]:


help(string)


# In[16]:


string.digits


# In[17]:


string.ascii_letters


# In[19]:


name = ''
if name[0] in string.digits:
    print('Name cannot start with a digit!')


# In[20]:


name = ''
if name and name[0] in string.digits:
    print('Name cannot start with a digit!')


# In[21]:


name = None
if name and name[0] in string.digits:
    print('Name cannot start with a digit!')


# In[22]:


name = 'Bob'
if name and name[0] in string.digits:
    print('Name cannot start with a digit!')


# In[23]:


name = '1Bob'
if name and name[0] in string.digits:
    print('Name cannot start with a digit!')


# In[ ]:




