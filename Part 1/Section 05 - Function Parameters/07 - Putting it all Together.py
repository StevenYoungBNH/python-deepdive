#!/usr/bin/env python
# coding: utf-8

# ### Putting it all Together

# Positionals Only: no extra positionals, no defaults (all positionals required)

# In[1]:


def func(a, b):
    print(a, b)


# In[2]:


func('hello', 'world')


# In[3]:


func(b='world', a='hello')


# Positionals Only: no extra positionals, defaults (some positionals optional)

# In[4]:


def func(a, b='world', c=10):
    print(a, b, c)


# In[5]:


func('hello')


# In[6]:


func('hello', c='!')


# Positionals Only: extra positionals, no defaults (all positionals required)

# In[7]:


def func(a, b, *args):
    print(a, b, args)


# In[8]:


func(1, 2, 'x', 'y', 'z')


# Note that we cannot call the function this way:

# In[9]:


func(b=2, a=1, 'x', 'y', 'z')


# Keywords Only: no positionals, no defaults (all keyword args required)

# In[10]:


def func(*, a, b):
    print(a, b)


# In[11]:


func(a=1, b=2)


# Keywords Only: no positionals, some defaults (not all keyword args required)

# In[12]:


def func(*, a=1, b):
    print(a, b)


# In[13]:


func(a=10, b=20)


# In[14]:


func(b=2)


# Keywords and Positionals: some positionals (no defaults), keywords (no defaults)

# In[15]:


def func(a, b, *, c, d):
    print(a, b, c, d)


# In[16]:


func(1, 2, c=3, d=4)


# In[17]:


func(1, 2, d=4, c=3)


# In[18]:


func(1, c=3, d=4, b=2)


# Keywords and Positionals: some positional defaults

# In[19]:


def func(a, b=2, *, c, d=4):
    print(a, b, c, d)


# In[20]:


func(1, c=3)


# In[21]:


func(c=3, a=1)


# In[22]:


func(1, 2, c=3, d=4)


# In[23]:


func(c=3, a=1, b=2, d=4)


# Keywords and Positionals: extra positionals

# In[24]:


def func(a, b=2, *args, c=3, d):
    print(a, b, args, c, d)


# In[25]:


func(1, 2, 'x', 'y', 'z', c=3, d=4)


# Note that if we are going to use the extra arguments, then we cannot actually use a default value for b:

# In[26]:


func(1, 'x', 'y', 'z', c=3, d=4)


# as you can see, **b** was assigned the value **x**

# Keywords and Positionals: no extra positionals, extra keywords

# In[27]:


def func(a, b, *, c, d=4, **kwargs):
    print(a, b, c, d, kwargs)


# In[28]:


func(1, 2, c=3, x=100, y=200, z=300)


# In[29]:


func(x=100, y=200, z=300, c=3, b=2, a=1)


# Keywords and Positionals: extra positionals, extra keywords

# In[30]:


def func(a, b, *args, c, d=4, **kwargs):
    print(a, b, args, c, d, kwargs)


# In[31]:


func(1, 2, 'x', 'y', 'z', c=3, d=5, x=100, y=200, z=300)


# Keywords and Positionals: only extra positionals and extra keywords

# In[32]:


def func(*args, **kwargs):
    print(args, kwargs)


# In[33]:


func(1, 2, 3, x=100, y=200, z=300)


# #### The Print Function

# In[34]:


help(print)


# In[35]:


print(1, 2, 3)


# In[36]:


print(1, 2, 3, sep='--')


# In[37]:


print(1, 2, 3, end='***\n')


# In[38]:


print(1, 2, 3, sep='\t', end='\t***\t')
print(4, 5, 6, sep='\t', end='\t***\n')


# #### Another Use Case

# In[39]:


def calc_hi_lo_avg(*args, log_to_console=False):
    hi = int(bool(args)) and max(args)
    lo = int(bool(args)) and min(args)
    avg = (hi + lo)/2
    if log_to_console:
        print("high={0}, low={1}, avg={2}".format(hi, lo, avg))
    return avg


# In[40]:


avg = calc_hi_lo_avg(1, 2, 3, 4, 5)
print(avg)


# In[41]:


avg = calc_hi_lo_avg(1, 2, 3, 4, 5, log_to_console=True)
print(avg)

