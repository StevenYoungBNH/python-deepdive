#!/usr/bin/env python
# coding: utf-8

# ### Callables

# A callable is an object that can be called (using the **()** operator), and always returns a value.
# 
# We can check if an object is callable by using the built-in function **callable**

# ##### Functions and Methods are callable

# In[1]:


callable(print)


# In[2]:


callable(len)


# In[3]:


l = [1, 2, 3]
callable(l.append)


# In[4]:


s = 'abc'
callable(s.upper)


# ##### Callables **always** return a value:

# In[5]:


result = print('hello')
print(result)


# In[6]:


l = [1, 2, 3]
result = l.append(4)
print(result)
print(l)


# In[7]:


s = 'abc'
result = s.upper()
print(result)


# ##### Classes are callable:

# In[8]:


from decimal import Decimal


# In[9]:


callable(Decimal)


# In[10]:


result = Decimal('10.5')
print(result)


# ##### Class instances may be callable:

# In[11]:


class MyClass:
    def __init__(self):
        print('initializing...')
        self.counter = 0
    
    def __call__(self, x=1):
        self.counter += x
        print(self.counter)


# In[12]:


my_obj = MyClass()


# In[13]:


callable(my_obj.__init__)


# In[14]:


callable(my_obj.__call__)


# In[15]:


my_obj()


# In[16]:


my_obj()


# In[17]:


my_obj(10)

