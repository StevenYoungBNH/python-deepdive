#!/usr/bin/env python
# coding: utf-8

# ### Challenge: Randomizing an Iterable using Sorted

# In[1]:


import random


# In[2]:


help(random.random)


# In[3]:


random.random()


# In[4]:


l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# In[5]:


sorted(l, key=lambda x: random.random())


# Of course, this works for any iterable:

# In[6]:


sorted('abcdefg', key = lambda x: random.random())


# And to get a string back instead of just a list:

# In[7]:


''.join(sorted('abcdefg', key = lambda x: random.random()))

