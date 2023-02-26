#!/usr/bin/env python
# coding: utf-8

# ### Copying Sets

# Just as with other container types, we need to differentiate between shallow copies and deep copies.

# Python sets implement a `copy` method that creates a shallow copy of the set. And, just as with lists, tuples, dictionaries, etc, we can also use unpacking to shallow copy sets. We can also just use the `set()` function to shallow copy one set into another.
# 
# Deep copies of sets can be done using the `deepcopy` function in the `copy` module.
# 
# The concepts and techniques are not new, so I won't spend much time on them.

# #### Shallow Copies using the `copy` method

# To illustrate the shallow copy vs deepcopy issues, we'll create our own mutable, but hashable type:

# In[1]:


class Person:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'Person(name={self.name})'


# In[2]:


p1 = Person('John')
p2 = Person('Eric')


# In[3]:


s1 = {p1, p2}


# In[4]:


s1


# Now let's make a shallow copy:

# In[5]:


s2 = s1.copy()


# In[6]:


s1 is s2


# As we can see the sets are not the same, however their contained elements **are**:

# In[7]:


p1.name = 'John Cleese'


# In[8]:


s1


# In[9]:


s2


# #### Shallow copies using unpacking

# We can use unpacking, similar to iterable unpacking to unpack one set into another:

# In[10]:


s3 = {*s2}


# In[11]:


s3 is s2


# In[12]:


s3


# In[13]:


p2.name = 'Eric Idle'


# In[14]:


print(s1)
print(s2)
print(s3)


# #### Shallow copies using the `set()` function

# In[15]:


s4 = set(s1)


# In[16]:


s4 is s1


# In[17]:


s4


# In[18]:


p1.name = 'Michael Palin'


# In[19]:


print(s1)
print(s2)
print(s3)
print(s4)


# #### Deep Copies

# In[20]:


from copy import deepcopy


# In[21]:


s5 = deepcopy(s1)


# In[22]:


s1 is s5


# In[23]:


s1


# In[24]:


s5


# In[25]:


p1.name = 'Terry Jones'


# In[26]:


print(s1)
print(s2)
print(s3)
print(s4)
print(s5)


# As you can see, the deep copy also made (deep) copies of each element in the set being (deep) copied.
