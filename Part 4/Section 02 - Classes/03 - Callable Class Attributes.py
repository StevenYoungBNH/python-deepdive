#!/usr/bin/env python
# coding: utf-8

# ### Callable Class Attributes

# Class attributes can be any object type, including callables such as functions:

# In[1]:


class Program:
    language = 'Python'
    
    def say_hello():
        print(f'Hello from {Program.language}!')


# In[2]:


Program.__dict__


# As we can see, the `say_hello` symbol is in the class dictionary.
# 
# We can also retrieve it using either `getattr` or dotted notation:

# In[3]:


Program.say_hello, getattr(Program, 'say_hello')


# And of course we can call it, since it is a callable:

# In[4]:


Program.say_hello()


# In[5]:


getattr(Program, 'say_hello')()


# We can even access it via the namespace dictionary as well:

# In[6]:


Program.__dict__['say_hello']()


# In[ ]:




