#!/usr/bin/env python
# coding: utf-8

# ### Python 3.6 - f-Strings

# Last highlight I want to mention are the new f-strings. For more details see PEP498.
# 
# f-Strings is short for *formatted string literals*

# You should already know how to format strings using the `format` method:

# In[1]:


# Using {}
'{} % {} = {}'.format(10, 3, 10 % 3)


# In[2]:


# Using {number}
'{1} % {2} = {0}'.format(10 % 3, 10, 3)


# In[3]:


# Using {name}
'{a} % {b} = {mod}'.format(a=10, b=3, mod=10 % 3)


# But now we can also do this:

# In[4]:


a = 10
b = 3
f'{a} % {b} = {a % b}'


# Basically in f-strings you can use expressions and reference variables inside your string which Python will then interpolate. Also uses all the existing string formatting options (`:0.5f` for example):

# In[5]:


a = 10 / 3

f'{a:0.5f}'


# So now, instead of writing:

# In[6]:


name = 'Python'
'{name} rocks'.format(name=name)


# which used the word `name` **three** times, we can simply say:

# In[7]:


name = 'Python'
f'{name} rocks!'


# Much more concise!

# How about with closures?

# In[8]:


def outer():
    name = 'Python'
    
    def inner():
        return f'{name} rocks!'
    
    return inner


# In[9]:


print(outer()())


# Woohoo!! That works too - note that we did not have to reference `name` (to make it a free variable in `inner`) before using it **inside** the f-string.

# I can see this open to abuse though...

# In[10]:


sq = lambda x: x**2
a = 10
b=1
print(f'{sq(a) if b > 5 else a}')

b=10
print(f'{sq(a) if b > 5 else a}')


# Or even this:

# In[11]:


a = 10
b = 1
print(f'{(lambda x: x**2)(a) if b > 5 else a}')

b=10
print(f'{(lambda x: x**2)(a) if b > 5 else a}')


# Lord help us... :-)
