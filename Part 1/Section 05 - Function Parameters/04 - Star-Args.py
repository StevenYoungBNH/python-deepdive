#!/usr/bin/env python
# coding: utf-8

# ### \*args

# Recall from iterable unpacking:

# In[10]:


a, b, *c = 10, 20, 'a', 'b'


# In[11]:


print(a, b)


# In[12]:


print(c)


# We can use a similar concept in function definitions to allow for arbitrary numbers of **positional** parameters/arguments:

# In[13]:


def func1(a, b, *args):
    print(a)
    print(b)
    print(args)


# In[14]:


func1(1, 2, 'a', 'b')


# A few things to note:

# 1. Unlike iterable unpacking, **\*args** will be a **tuple**, not a list.
# 
# 2. The name of the parameter **args** can be anything you prefer
# 
# 3. You cannot specify positional arguments **after** the **\*args** parameter - this does something different that we'll cover in the next lecture.

# In[15]:


def func1(a, b, *my_vars):
    print(a)
    print(b)
    print(my_vars)


# In[16]:


func1(10, 20, 'a', 'b', 'c')


# In[17]:


def func1(a, b, *c, d):
    print(a)
    print(b)
    print(c)
    print(d)


# In[18]:


func1(10, 20, 'a', 'b', 100)


# Let's see how we might use this to calculate the average of an arbitrary number of parameters.

# In[19]:


def avg(*args):
    count = len(args)
    total = sum(args)
    return total/count


# In[20]:


avg(2, 2, 4, 4)


# But watch what happens here:

# In[21]:


avg()


# The problem is that we passed zero arguments.
# 
# We can fix this in one of two ways:

# In[22]:


def avg(*args):
    count = len(args)
    total = sum(args)
    if count == 0:
        return 0
    else:
        return total/count


# In[23]:


avg(2, 2, 4, 4)


# In[24]:


avg()


# But we may not want to allow specifying zero arguments, in which case we can split our parameters into a required (non-defaulted) positional argument, and the rest:

# In[25]:


def avg(a, *args):
    count = len(args) + 1
    total = a + sum(args)
    return total/count


# In[26]:


avg(2, 2, 4, 4)


# In[27]:


avg()


# As you can see, an exception occurs if we do not specify at least one argument.

# #### Unpacking an iterable into positional arguments

# In[28]:


def func1(a, b, c):
    print(a)
    print(b)
    print(c)


# In[29]:


l = [10, 20, 30]


# This will **not** work:

# In[30]:


func1(l)


# The function expects three positional arguments, but we only supplied a single one (albeit a list).
# 
# But we could unpack the list, and **then** pass it to as the function arguments:

# In[31]:


*l,


# In[32]:


func1(*l)


# What about mixing positional and keyword arguments with this?

# In[33]:


def func1(a, b, c, *d):
    print(a)
    print(b)
    print(c)
    print(d)


# In[34]:


func1(10, c=20, b=10, 'a', 'b')


# Recall that once a keyword argument is used in a function call, we **cannot** use positional arguments after that. 
# 
# However, in the next lecture we'll look at how to address this issue.
