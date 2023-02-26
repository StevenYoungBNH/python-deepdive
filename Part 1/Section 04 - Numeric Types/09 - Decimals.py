#!/usr/bin/env python
# coding: utf-8

# ### Decimals

# In[1]:


import decimal


# In[2]:


from decimal import Decimal


# Decimals have context, that can be used to specify rounding and precision (amongst other things)

# Contexts can be local (temporary contexts) or global (default)

# #### Global Context

# In[3]:


g_ctx  = decimal.getcontext()


# In[4]:


g_ctx.prec


# In[5]:


g_ctx.rounding


# We can change settings in the global context:

# In[6]:


g_ctx.prec = 6


# In[7]:


g_ctx.rounding = decimal.ROUND_HALF_UP


# And if we read this back directly from the global context:

# In[8]:


decimal.getcontext().prec


# In[9]:


decimal.getcontext().rounding


# we see that the global context was indeed changed.

# #### Local Context

# The ``localcontext()`` function will return a context manager that we can use with a ``with`` statement:

# In[10]:


with decimal.localcontext() as ctx:
    print(ctx.prec)
    print(ctx.rounding)


# Since no argument was specified in the ``localcontext()`` call, it provides us a context manager that uses a copy of the global context.

# Modifying the local context has no effect on the global context

# In[11]:


with decimal.localcontext() as ctx:
    ctx.prec = 10
    print('local prec = {0}, global prec = {1}'.format(ctx.prec, g_ctx.prec))


# #### Rounding

# In[12]:


decimal.getcontext().rounding


# The rounding mechanism is ROUND_HALF_UP because we set the global context to that earlier in this notebook. Note that normally the default is ROUND_HALF_EVEN.
# 
# So we first reset our global context rounding to that:

# In[13]:


decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN


# In[14]:


x = Decimal('1.25')
y = Decimal('1.35')
print(round(x, 1))
print(round(y, 1))


# Let's change the rounding mechanism in the global context to ROUND_HALF_UP:

# In[15]:


decimal.getcontext().rounding = decimal.ROUND_HALF_UP


# In[16]:


x = Decimal('1.25')
y = Decimal('1.35')
print(round(x, 1))
print(round(y, 1))


# As you may have realized, changing the global context is a pain if you need to constantly switch between different precisions and rounding algorithms. Also, it could introduce bugs if you forget that you changed the global context somewhere further up in your module.
# 
# For this reason, it is usually better to use a local context manager instead:

# First we reset our global context rounding to the default:

# In[17]:


decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN


# In[18]:


x = Decimal('1.25')
y = Decimal('1.35')
print(round(x, 1), round(y, 1))
with decimal.localcontext() as ctx:
    ctx.rounding = decimal.ROUND_HALF_UP
    print(round(x, 1), round(y, 1))
print(round(x, 1), round(y, 1))

