#!/usr/bin/env python
# coding: utf-8

# ### Coercing Floats to Integers

# #### Truncation

# In[1]:


from math import trunc


# In[2]:


trunc(10.3), trunc(10.5), trunc(10.6)


# In[3]:


trunc(-10.6), trunc(-10.5), trunc(-10.3)


# The **int** constructor uses truncation when a float is passed in:

# In[4]:


int(10.3), int(10.5), int(10.6)


# In[5]:


int(-10.5), int(-10.5), int(-10.4)


# #### Floor

# In[6]:


from math import floor


# In[7]:


floor(10.4), floor(10.5), floor(10.6)


# In[8]:


floor(-10.4), floor(-10.5), floor(-10.6)


# #### Ceiling

# In[9]:


from math import ceil


# In[10]:


ceil(10.4), ceil(10.5), ceil(10.6)


# In[11]:


ceil(-10.4), ceil(-10.5), ceil(-10.6)


# In[ ]:




