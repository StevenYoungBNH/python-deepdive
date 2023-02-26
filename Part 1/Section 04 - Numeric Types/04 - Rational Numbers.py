#!/usr/bin/env python
# coding: utf-8

# ## Rational Numbers

# In[1]:


from fractions import Fraction


# We can get some info on the Fraction class:

# In[2]:


help(Fraction)


# We can create Fraction objects in a variety of ways:

# Using integers:

# In[3]:


Fraction(1)


# In[4]:


Fraction(1, 3)


# Using rational numbers:

# In[5]:


x = Fraction(2, 3)
y = Fraction(3, 4)
# 2/3 / 3/4 --> 2/3 * 4/3 --> 8/9
Fraction(x, y)


# Using floats:

# In[6]:


Fraction(0.125)


# In[7]:


Fraction(0.5)


# Using strings:

# In[8]:


Fraction('10.5')


# In[9]:


Fraction('22/7')


# Fractions are automatically reduced:

# In[10]:


Fraction(8, 16)


# Negative sign is attached to the numerator:

# In[11]:


Fraction(1, -4)


# Standard arithmetic operators are supported:

# In[12]:


Fraction(1, 3) + Fraction(1, 3) + Fraction(1, 3)


# In[13]:


Fraction(1, 2) * Fraction(1, 4)


# In[14]:


Fraction(1, 2) / Fraction(1, 3)


# We can recover the numerator and denominator (integers):

# In[15]:


x = Fraction(22, 7)
print(x.numerator)
print(x.denominator)


# Since floats have **finite** precision, any float can be converted to a rational number:

# In[16]:


import math
x = Fraction(math.pi)
print(x)
print(float(x))


# In[17]:


x = Fraction(math.sqrt(2))
print(x)


# Note that these rational values are approximations to the irrational numbers $\pi$ and $\sqrt{2}$

# **Beware!!**

# Float number representations (as we will examine in future lessons) do not always have an exact representation.

# The number 0.125 (1/8) **has** an exact representation:

# In[18]:


Fraction(0.125)


# and so we see the expected equivalent fraction.
# 
# But, 0.3 (3/10) does **not** have an exact representation:

# In[19]:


Fraction(3, 10)


# but

# In[20]:


Fraction(0.3)


# We will study this in upcoming lessons.
# 
# But for now, let's just see a quick explanation:

# In[21]:


x = 0.3


# In[22]:


print(x)


# Everything looks ok here - why am I saying 0.3 (float) is just an approximation?
# 
# Python is trying to format the displayed value for readability - so it rounds the number for a better display format!
# 
# We can instead choose to display the value using a certain number of digits:

# In[23]:


format(x, '.5f')


# At 5 digits after the decimal, we might still think 0.3 is an exact representation.
# 
# But let's display a few more digits:

# In[24]:


format(x, '.15f')


# Hmm... 15 digits and still looking good!
# 
# How about 25 digits...

# In[25]:


format(x, '.25f')


# Now we see that **x** is not quite 0.3...

# In fact, we can quantify the delta this way:

# In[26]:


delta = Fraction(0.3) - Fraction(3, 10)


# Theoretically, delta should be 0, but it's not:

# In[27]:


delta == 0


# In[28]:


delta


# **delta** is a very small number, the above fraction...
# 
# As a float:

# In[29]:


float(delta)


# #### Constraining the denominator

# In[30]:


x = Fraction(math.pi)
print(x)
print(format(float(x), '.25f'))


# In[31]:


y = x.limit_denominator(10)
print(y)
print(format(float(y), '.25f'))


# In[32]:


y = x.limit_denominator(100)
print(y)
print(format(float(y), '.25f'))


# In[33]:


y = x.limit_denominator(500)
print(y)
print(format(float(y), '.25f'))

