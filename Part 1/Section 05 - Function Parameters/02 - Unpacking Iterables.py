#!/usr/bin/env python
# coding: utf-8

# ### Unpacking Iterables

# #### Side Note on Tuples

# This is a tuple:

# In[1]:


a = (1, 2, 3)


# In[2]:


type(a)


# This is also a tuple:

# In[3]:


a = 1, 2, 3


# In[4]:


type(a)


# In fact what defines a tuple is not **()**, but the **,** (comma)

# To create a tuple with a single element:

# In[5]:


a = (1)


# will not work!!

# In[6]:


type(a)


# Instead, we have to use a comma:

# In[7]:


a = (1,)


# In[8]:


type(a)


# And in fact, we don't even need the **()**:

# In[9]:


a = 1,


# In[10]:


type(a)


# The only exception is to create an empty tuple:

# In[11]:


a = ()


# In[12]:


type(a)


# Or we can use the tuple constructor:

# In[13]:


a = tuple()


# In[14]:


type(a)


# #### Unpacking

# Unpacking is a way to split an iterable object into individual variables contained in a list or tuple: 

# In[15]:


l = [1, 2, 3, 4]


# In[16]:


a, b, c, d = l


# In[17]:


print(a, b, c, d)


# Strings are iterables too:

# In[18]:


a, b, c = 'XYZ'
print(a, b, c)


# #### Swapping Two Variables

# Here's a quick application of unpacking to swap the values of two variables.

# First we look at the "traditional" way you would have to do it in other languages such as Java:

# In[19]:


a = 10
b = 20
print("a={0}, b={1}".format(a, b))

tmp = a
a = b
b = tmp
print("a={0}, b={1}".format(a, b))


# But using unpacking we can simplify this:

# In[20]:


a = 10
b = 20
print("a={0}, b={1}".format(a, b))

a, b = b, a
print("a={0}, b={1}".format(a, b))


# In fact, we can even simplify the initial assignment of values to a and b as follows:

# In[21]:


a, b = 10, 20
print("a={0}, b={1}".format(a, b))

a, b = b, a
print("a={0}, b={1}".format(a, b))


# #### Unpacking Unordered Objects

# In[22]:


dict1 = {'p': 1, 'y': 2, 't': 3, 'h': 4, 'o': 5, 'n': 6}


# In[23]:


dict1


# In[24]:


for c in dict1:
    print(c)


# In[25]:


a, b, c, d, e, f = dict1
print(a)
print(b)
print(c)
print(d)
print(e)
print(f)


# Note that this order is not guaranteed. You can always use an OrderedDict if that is a requirement.

# The same applies to sets.

# In[26]:


s = {'p', 'y', 't', 'h', 'o', 'n'}


# In[27]:


type(s)


# In[28]:


print(s)


# In[29]:


for c in s:
    print(c)


# In[30]:


a, b, c, d, e, f = s


# In[31]:


print(a)
print(b)
print(c)
print(d)
print(e)
print(f)

