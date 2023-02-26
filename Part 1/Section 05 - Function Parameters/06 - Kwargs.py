#!/usr/bin/env python
# coding: utf-8

# ### **kwargs

# In[5]:


def func(**kwargs):
    print(kwargs)


# In[6]:


func(x=100, y=200)


# We can also use it in conjunction with **\*args**: 

# In[7]:


def func(*args, **kwargs):
    print(args)
    print(kwargs)


# In[8]:


func(1, 2, a=100, b=200)


# Note: You cannot do the following:

# In[9]:


def func(*, **kwargs):
    print(kwargs)


# There is no need to even do this, since **\*\*kwargs** essentially indicates no more positional arguments.

# In[10]:


def func(a, b, **kwargs):
    print(a)
    print(b)
    print(kwargs)


# In[11]:


func(1, 2, x=100, y=200)


# Also, you cannot specify parameters **after** **\*\*kwargs** has been used:

# In[12]:


def func(a, b, **kwargs, c):
    pass


# If you want to specify both specific keyword-only arguments and **\*\*kwargs** you will need to first get to a point where you can define a keyword-only argument (i.e. exhaust the positional arguments, using either **\*args** or just **\***)

# In[13]:


def func(*, d, **kwargs):
    print(d)
    print(kwargs)


# In[14]:


func(d=1, x=100, y=200)

