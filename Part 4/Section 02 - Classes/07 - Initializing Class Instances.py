#!/usr/bin/env python
# coding: utf-8

# ### Initializing Class Instances

# When we create a new instance of a class two separate things are happening:
# 1. The object instance is **created**
# 2. The object instance is then further **initialized**

# We can "intercept" both the creating and initialization phases, by using special methods `__new__` and `__init__`.
# 
# We'll come back to `__new__` later. For now we'll focus on `__init__`.

# What's important to remember, is that `__init__` is an **instance method**. By the time `__init__` is called, the new object has **already** been created, and our `__init__` function defined in the class is now treated like a **method** bound to the instance.

# In[1]:


class Person:
    def __init__(self):
        print(f'Initializing a new Person object: {self}')


# In[2]:


p = Person()


# And we can see that `p` has the same memory address:

# In[3]:


hex(id(p))


# Because `__init__` is an instance method, we have access to the object (instance) state within the method, so we can use it to manipulate the object state:

# In[4]:


class Person:
    def __init__(self, name):
        self.name = name


# In[5]:


p = Person('Eric')


# In[6]:


p.__dict__


# What actually happens is that after the new instance has been created, Python sees and automatically calls `<instance>.__init__(self, *args, **kwargs)`

# In[14]:


p.__init__( "Jim")


# In[15]:


p.__dict__


# So this is no different than if we had done it this way:

# In[7]:


class Person:
    def initialize(self, name):
        self.name = name


# In[8]:


p = Person()


# In[9]:


p.__dict__


# In[10]:


p.initialize('Eric')


# In[11]:


p.__dict__


# But by using the `__init__` method both these things are done automatically for us.
# 
# Just remember that by the time `__init__` is called, the instance has **already** been created, and `__init__` is an instance method.
