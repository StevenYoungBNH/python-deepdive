#!/usr/bin/env python
# coding: utf-8

# ### Class Attributes

# As we saw, when we create a class Python automatically builds-in properties and behaviors into our class object, like making it callable, and properties like `__name__`.

# In[1]:


class Person:
    pass


# In[2]:


Person.__name__


# `__name__` is a **class attribute**. We can add our own class attributes easily this way:

# In[3]:


class Program:
    language = 'Python'
    version = '3.6'


# In[4]:


Program.__name__


# In[5]:


Program.language


# In[6]:


Program.version


# Here we used "dotted notation" to access the class attributes. In fact we can also use dotted notation to set the class attribute:

# In[7]:


Program.version = '3.7'


# In[8]:


Program.version


# But we can also use the functions `getattr` and `setattr` to read and write these attributes:

# In[9]:


getattr(Program, 'version')


# In[10]:


setattr(Program, 'version', '3.6')


# In[11]:


Program.version, getattr(Program, 'version')


# Python is a dynamic language, and we can create attributes at run-time, outside of the class definition itself:

# In[12]:


Program.x = 100


# Using dotted notation we added an attribute `x` to the Person class:

# In[13]:


Program.x, getattr(Program, 'x')


# We could also just have used a `setattr` function call:

# In[14]:


setattr(Program, 'y', 200)


# In[15]:


Program.y, getattr(Program, 'y')


# So where is the state stored? Usually in a dictionary that is attached to the **class** object (often referred to as the **namespace** of the class):

# In[16]:


Program.__dict__


# As you can see that dictionary contains our attributes: `language`, `version`, `x`, `y` with their corresponding current values.

# Notice also that `Program.__dict__` does not return a dictionary, but a `mappingproxy` object - this is essentially a read-only dictionary that we cannot modify directly (but we can modify it by using `setattr`, or dotted notation).

# For example, if we change the value of an attribute:

# In[17]:


setattr(Program, 'x', -10)


# We'll see this reflected in the underlying dictionary:

# In[18]:


Program.__dict__


# #### Deleting Attributes

# So, we can create and mutate class attributes at run-time. Can we delete attributes too?
# 
# The answer of course is yes. We can either use the `del` keyword, or the `delattr` function:

# In[19]:


del Program.x


# In[20]:


Program.__dict__


# In[21]:


delattr(Program, 'y')


# #### Direct Namespace Access

# In[22]:


Program.__dict__


# Although `__dict__` returns a `mappingproxy` object, it still is a hash map and essentially behaves like a read-only dictionary:

# In[23]:


Program.__dict__['language']


# In[24]:


list(Program.__dict__.items())


# One word of caution: not every attribute that a class has lives in that dictionary (we'll come back to this later).
# 
# For example, you'll notice that the `__name__` attribute is not there:

# In[25]:


Program.__name__


# In[26]:


__name__ in Program.__dict__

