#!/usr/bin/env python
# coding: utf-8

# ## Everything is an Object

# In[1]:


a = 10


# **a** is an object of type **int**, i.e. **a** is an instance of the **int** class.

# In[2]:


print(type(a))


# If **int** is a class, we should be able to declare it using standard class instatiation:

# In[3]:


b = int(10)


# In[4]:


print(b)
print(type(b))


# We can even request the class documentation:

# In[5]:


help(int)


# As we see from the docs, we can even create an **int** using an overloaded constructor:

# In[6]:


b = int('10', base=2)


# In[7]:


print(b)
print(type(b))


# ### Functions are Objects too
# ---

# In[8]:


def square(a):
    return a ** 2


# In[9]:


type(square)


# In fact, we can even assign them to a variable:

# In[10]:


f = square


# In[11]:


type(f)


# In[12]:


f is square


# In[13]:


f(2)


# In[14]:


type(f(2))


# A function can return a function

# In[15]:


def cube(a):
    return a ** 3


# In[16]:


def select_function(fn_id):
    if fn_id == 1:
        return square
    else:
        return cube


# In[17]:


f = select_function(1)
print(hex(id(f)))
print(hex(id(square)))
print(hex(id(cube)))
print(type(f))
print('f is square: ', f is square)
print('f is cube: ', f is cube)
print(f)
print(f(2))


# In[18]:


f = select_function(2)
print(hex(id(f)))
print(hex(id(square)))
print(hex(id(cube)))
print(type(f))
print('f is square: ', f is square)
print('f is cube: ', f is cube)
print(f)
print(f(2))


# We could even call it this way:

# In[19]:


select_function(1)(5)


# A Function can be passed as an argument to another function
# 
# (This example is pretty useless, but it illustrates the point effectively)

# In[20]:


def exec_function(fn, n):
    return fn(n)


# In[21]:


result = exec_function(cube, 2)
print(result)


# We will come back to functions as arguments **many** more times throughout this course!
