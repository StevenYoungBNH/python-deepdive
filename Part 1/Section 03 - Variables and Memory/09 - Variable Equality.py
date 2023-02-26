#!/usr/bin/env python
# coding: utf-8

# ## Variable Equality

# From the previous lecture we know that **a** and **b** will have a **shared** reference:

# In[1]:


a = 10
b = 10

print(hex(id(a)))
print(hex(id(b)))


# When we use the **is** operator, we are comparing the memory address **references**:

# In[2]:


print("a is b: ", a is b)


# But if we use the **==** operator, we are comparing the **contents**:

# In[3]:


print("a == b:", a == b)


# The following however, do not have a shared reference:

# In[4]:


a = [1, 2, 3]
b = [1, 2, 3]

print(hex(id(a)))
print(hex(id(b)))


# Although they are not the same objects, they do contain the same "values":

# In[5]:


print("a is b: ", a is b)
print("a == b", a == b)


# Python will attempt to compare values as best as possible, for example:

# In[6]:


a = 10
b = 10.0


# These are **not** the same reference, since one object is an **int** and the other is a **float**

# In[7]:


print(type(a))
print(type(b))


# In[8]:


print(hex(id(a)))
print(hex(id(b)))


# In[9]:


print('a is b:', a is b)
print('a == b:', a == b)


# So, even though *a* is an integer 10, and *b* is a float 10.0, the values will still compare as equal.

# In fact, this will also have the same behavior:

# In[10]:


c = 10 + 0j
print(type(c))


# In[11]:


print('a is c:', a is c)
print('a == c:', a == c)


# ### The None Object
# ----

# **None** is a built-in "variable" of type *NoneType*.
# 
# Basically the keyword **None** is a reference to an object instance of *NoneType*.
# 
# NoneType objects are immutable! Python's memory manager will therefore use shared references to the None object.

# In[12]:


print(None)


# In[13]:


hex(id(None))


# In[14]:


type(None)


# In[15]:


a = None
print(type(a))
print(hex(id(a)))


# In[16]:


a is None


# In[17]:


a == None


# In[18]:


b = None
hex(id(b))


# In[19]:


a is b


# In[20]:


a == b


# In[21]:


l = []


# In[22]:


type(l)


# In[23]:


l is None


# In[24]:


l == None

