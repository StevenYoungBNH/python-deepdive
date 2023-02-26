#!/usr/bin/env python
# coding: utf-8

# ## Python Optimizations: Interning

# Earlier, we saw shared references being created automatically by Python:

# In[1]:


a = 10
b = 10
print(id(a))
print(id(b))


# Note how `a` and `b` reference the same object.
# 
# But consider the following example:

# In[2]:


a = 500
b = 500
print(id(a))
print(id(b))


# As you can see, the variables `a` and `b` do **not** point to the same object!
# 
# This is because Python pre-caches integer objects in the range [-5, 256]

# So for example:

# In[3]:


a = 256
b = 256
print(id(a))
print(id(b))


# and

# In[4]:


a = -5
b = -5
print(id(a))
print(id(b))


# do have the same reference.
# 
# This is called **interning**: Python **interns** the integers in the range [-5, 256].

# The integers in the range [-5, 256] are essentially **singleton** objects.

# In[5]:


a = 10
b = int(10)
c = int('10')
d = int('1010', 2)


# In[6]:


print(a, b, c, d)


# In[7]:


a is b


# In[8]:


a is c


# In[9]:


a is d


# As you can see, all these variables were created in different ways, but since the integer object with value 10 behaves like a singleton, they all ended up pointing to the **same** object in memory.
