#!/usr/bin/env python
# coding: utf-8

# ## Floats - Internal Representation

# The ``float`` class can be used to represent real numbers.

# In[1]:


help(float)


# The ``float`` class has a single constructor, which can take a number or a string and will attempt to convert it to a float.

# In[2]:


float(10)


# In[3]:


float(3.14)


# In[4]:


float('0.1')


# However, strings that represent fractions cannot be converted to floats, unlike the Fraction class we saw earlier.

# In[5]:


float('22/7')


# If you really want to get a float from a string such as ``'22/7'``, you could first create a ``Fraction``, then create a ``float`` from that:

# In[ ]:


from fractions import Fraction


# In[ ]:


float(Fraction('22/7'))


# Floats do not always have an exact representation:

# In[ ]:


print(0.1)


# Although this looks like ``0.1`` exactly, we need to reveal more digits after the decimal point to see what's going on:

# In[ ]:


format(0.1, '.25f')


# However, certain numbers can be represented exactly in a binary fraction expansion:

# In[ ]:


format(0.125, '.25f')


# This is because 0.125 is precisely 1/8, or 1/(2^3)
