#!/usr/bin/env python
# coding: utf-8

# ### Named Tuples - Application - Returning Multiple Values

# We already know that we can easily return multiple values from a function by using a tuple:

# In[21]:


from random import randint, random

def random_color():
    red = randint(0, 255)
    green = randint(0,255)
    blue = randint(0, 255)
    alpha = round(random(), 2)
    return red, green, blue, alpha


# In[23]:


random_color()


# So of course, we could call the function this and unpack the results at the same time:

# In[25]:


red, green, blue, alpha = random_color()


# In[26]:


print(f'red={red}, green={green}, blue={blue}, alpha={alpha}')


# But it might be nicer to use a named tuple:

# In[27]:


from collections import namedtuple


# In[28]:


Color = namedtuple('Color', 'red green blue alpha')

def random_color():
    red = randint(0, 255)
    green = randint(0,255)
    blue = randint(0, 255)
    alpha = round(random(), 2)
    return Color(red, green, blue, alpha)


# In[29]:


color = random_color()


# In[30]:


color.red


# In[31]:


color

