#!/usr/bin/env python
# coding: utf-8

# ### Classes are Callable

# As we saw earlier, one of the things Python does for us when we create a class is to make it callable.
# 
# Calling a class creates a new instance of the class - an object of that particular type.

# In[1]:


class Program:
    language = 'Python'
    
    def say_hello():
        print(f'Hello from {Program.language}!')


# In[2]:


p = Program()


# In[3]:


type(p)


# In[4]:


isinstance(p, Program)


# These instances have their own namespace, and their own `__dict__` that is distinct from the class `__dict__`:

# In[5]:


p.__dict__


# In[6]:


Program.__dict__


# Instances also have attributes that may not be visible in their `__dict__` (they are being stored elsewhere, as we'll examine later):

# In[7]:


p.__class__


# Although we can use `__class__` we can also use `type`:

# In[8]:


type(p) is p.__class__


# Generally we use `type` instead of using `__class__` just like we usually use `len()` instead of accessing `__len__`.

# Why? Well, one reason is that people can mess around with the `__class__` attribute:

# In[9]:


class MyClass:
    pass


# In[10]:


m = MyClass()


# In[11]:


type(m), m.__class__


# But look at what happens here:

# In[12]:


class MyClass:
    __class__ = str


# In[13]:


m = MyClass()


# In[14]:


type(m), m.__class__


# So as you can see, `type` wasn't fooled!

# In[ ]:




