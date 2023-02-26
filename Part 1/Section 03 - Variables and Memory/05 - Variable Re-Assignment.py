#!/usr/bin/env python
# coding: utf-8

# ## Variable Re-Assignment

# Notice how the memory address of **a** is different every time.

# In[1]:


a = 10
hex(id(a))


# In[2]:


a = 15
hex(id(a))


# In[3]:


a = 5
hex(id(a))


# In[4]:


a = a + 1
hex(id(a))


# However, look at this:

# In[5]:


a = 10
b = 10
print(hex(id(a)))
print(hex(id(b)))


# The memory addresses of both **a** and **b** are the same!! 
# 
# We'll revisit this in a bit to explain what is going on.
