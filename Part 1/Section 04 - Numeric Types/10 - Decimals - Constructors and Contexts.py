#!/usr/bin/env python
# coding: utf-8

# ### Decimals: Constructors and Contexts

# The **Decimal** constructor can handle a variety of data types

# In[1]:


import decimal
from decimal import Decimal


# #### Integers

# In[2]:


Decimal(10)


# In[3]:


Decimal(-10)


# #### Strings

# In[4]:


Decimal('0.1')


# In[5]:


Decimal('-3.1415')


# #### Tuples

# In[6]:


Decimal ((0, (3,1,4,1,5), -4))


# In[7]:


Decimal((1, (1,2,3,4), -3))


# In[8]:


Decimal((0, (1,2,3), 3))


# #### But don't use Floats

# In[9]:


format(0.1, '.25f')


# In[10]:


Decimal(0.1)


# As you can see, since we passed an approximate binary float to the Decimal constructor it did it's best to represent that binary float **exactly**!!

# So, instead, use strings or tuples in the Decimal constructor.

# #### Context Precision and the Constructor

# The context precision does nto affect the precision used when creating a Decimal object - those are independent of each other.

# Let's set our global (default) context to a precision of 2

# In[11]:


decimal.getcontext().prec = 2


# Now we can create decimal numbers of higher precision than that:

# In[12]:


a = Decimal('0.12345')
b = Decimal('0.12345')


# In[13]:


a


# In[14]:


b


# But when we add those two numbers up, the context precision will matter:

# In[15]:


a+b


# As you can see, we ended up with a sum that was rounded to 2 digits after the decimal point (precision = 2)

# #### Local and Global Contexts are Independent

# In[16]:


decimal.getcontext().prec = 6


# In[17]:


decimal.getcontext().rounding


# In[18]:


a = Decimal('0.12345')
b = Decimal('0.12345')
print(a + b)
with decimal.localcontext() as ctx:
    ctx.prec = 2
    c = a + b
    print('c within local context: {0}'.format(c))
print('c within global context: {0}'.format(c))


# Since **c** was created within the local context by adding **a** and **b**, and the local context had a precision of 2, **c** was rounded to 2 digits after the decimal point.
# 
# Once the local context is destroyed (after the **with** block), the variable **c** still exists, and its precision is **still** just 2 - it doesn't magically suddenly get the global context's precision of 6.
