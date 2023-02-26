#!/usr/bin/env python
# coding: utf-8

# ### Positional Arguments

# In[1]:


def my_func(a, b, c):
    print("a={0}, b={1}, c={2}".format(a, b, c))


# In[2]:


my_func(1, 2, 3)


# #### Default Values

# In[3]:


def my_func(a, b=2, c=3):
    print("a={0}, b={1}, c={2}".format(a, b, c))


# Note that once a parameter is assigned a default value, **all** parameters thereafter **must** be asigned a default value too!

# For example, this will not work:

# In[4]:


def fn(a, b=2, c):
    print(a, b, c)


# In[5]:


def my_func(a, b=2, c=3):
    print("a={0}, b={1}, c={2}".format(a, b, c))


# In[6]:


my_func(10, 20, 30)


# In[7]:


my_func(10, 20)


# In[8]:


my_func(10)


# Since **a** does not have a default value, it **must** be specified:

# In[9]:


my_func()


# #### Keyword Arguments (named arguments)

# Positional arguments, can **optionally**, be specified using their corresponding parameter name.
# 
# This allows us to pass the arguments without using the positional assignment:

# In[10]:


def my_func(a, b=2, c=3):
    print("a={0}, b={1}, c={2}".format(a, b, c))


# In[11]:


my_func(c=30, b=20, a=10)


# In[12]:


my_func(10, c=30, b=20)


# Note that once a keyword argument has been used, **all** arguments thereafter **must** also be named:

# In[13]:


my_func(10, b=20, 30)


# However, if a parameter has a default value, it *can* be omitted from the argument list, named or not:

# In[15]:


my_func(10, c=30)


# In[16]:


my_func(a=30, c=10)


# In[17]:


my_func(c=10, a=30)

