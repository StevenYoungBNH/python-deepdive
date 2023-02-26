#!/usr/bin/env python
# coding: utf-8

# ### Nonlocal Scopes

# Functions defined inside anther function can reference variables from that enclosing scope, just like functions can reference variables from the global scope.

# In[1]:


def outer_func():
    x = 'hello'
    
    def inner_func():
        print(x)
    
    inner_func()


# In[2]:


outer_func()


# In fact, any level of nesting is supported since Python just keeps looking in enclosing scopes until it finds what it needs (or fails to find it by the time it finishes looking in the built-in scope, in which case a runtime error occurrs.)

# In[3]:


def outer_func():
    x = 'hello'
    def inner1():
        def inner2():
            print(x)
        inner2()
    inner1()


# In[4]:


outer_func()


# But if we **assign** a value to a variable, it is considered part of the local scope, and potentially **masks** enclsogin scope variable names:

# In[5]:


def outer():
    x = 'hello'
    def inner():
        x = 'python'
    inner()
    print(x)


# In[6]:


outer()


# As you can see, **x** in **outer** was not changed.

# To achieve this, we can use the **nonlocal** keyword:

# In[7]:


def outer():
    x = 'hello'
    def inner():
        nonlocal x
        x = 'python'
    inner()
    print(x)


# In[8]:


outer()


# Of course, this can work at any level as well:

# In[9]:


def outer():
    x = 'hello'
    
    def inner1():
        def inner2():
            nonlocal x
            x = 'python'
        inner2()
    inner1()
    print(x)


# In[10]:


outer()


# How far Python looks up the chain depends on the first occurrence of the variable name in an enclosing scope.
# 
# Consider the following example:

# In[11]:


def outer():
    x = 'hello'
    def inner1():
        x = 'python'
        def inner2():
            nonlocal x
            x = 'monty'
        print('inner1 (before):', x)
        inner2()
        print('inner1 (after):', x)
    inner1()
    print('outer:', x)


# In[12]:


outer()


# What happened here, is that `x` in `inner1` **masked** `x` in `outer`. But `inner2` indicated to Python that `x` was nonlocal, so the first local variable up in the enclosing scope chain Python found was the one in `inner1`, hence `x` in `inner2` is actually referencing `x` that is local to `inner1`

# We can change this behavior by making the variable `x` in `inner` nonlocal as well:

# In[13]:


def outer():
    x = 'hello'
    def inner1():
        nonlocal x
        x = 'python'
        def inner2():
            nonlocal x
            x = 'monty'
        print('inner1 (before):', x)
        inner2()
        print('inner1 (after):', x)
    inner1()
    print('outer:', x)


# In[14]:


outer()


# In[15]:


x = 100
def outer():
    x = 'python'  # masks global x
    def inner1():
        nonlocal x  # refers to x in outer
        x = 'monty' # changed x in outer scope
        def inner2():
            global x  # refers to x in global scope
            x = 'hello'
        print('inner1 (before):', x)
        inner2()
        print('inner1 (after):', x)
    inner1()
    print('outer', x)    


# In[16]:


outer()
print(x)


# But this will not work. In `inner` Python is looking for a local variable called `x`. `outer` has a label called `x`, but it is a global variable, not a local one - hence Python does not find a local variable in the scope chain.

# In[17]:


x = 100
def outer():
    global x
    x = 'python'
    
    def inner():
        nonlocal x
        x = 'monty'
    inner()


# In[ ]:




