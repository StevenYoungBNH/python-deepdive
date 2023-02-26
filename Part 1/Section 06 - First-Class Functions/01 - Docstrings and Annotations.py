#!/usr/bin/env python
# coding: utf-8

# ### Docstrings and Annotations

# #### Docstrings

# When we call **help()** on a class, function, module, etc, Python will typically display some information:

# In[1]:


help(print)


# We can define such help using docstrings and annotations.

# In[2]:


def my_func(a, b):
    return a*b


# In[3]:


help(my_func)


# Pretty bare! So let's add some additional help:

# In[4]:


def my_func(a, b):
    'Returns the product of a and b'
    return a*b


# In[5]:


help(my_func)


# Docstrings can span multiple lines using a multi-line string literal:

# In[6]:


def fact(n):
    '''Calculates n! (factorial function)
    
    Inputs:
        n: non-negative integer
    Returns:
        the factorial of n
    '''
    
    if n < 0:
        '''Note that this is not part of the docstring!'''
        return 1
    else:
        return n * fact(n-1)
    
    


# In[7]:


help(fact)


# Docstrings, when found, are simply attached to the function in the `__doc__` property:

# In[8]:


fact.__doc__


# And the Python **help()** function simply returns the contents of `__doc__`

# #### Annotations

# We can also add metadata annotations to a function's parameters and return. These metadata annotations can be any **expression** (string, type, function call, etc)

# In[9]:


def my_func(a:'annotation for a', 
            b:'annotation for b')->'annotation for return':
    
    return a*b


# In[10]:


help(my_func)


# The annotations can be any expression, not just strings:

# In[11]:


x = 3
y = 5
def my_func(a: str) -> 'a repeated ' + str(max(3, 5)) + ' times':
	return a*max(x, y)


# In[12]:


help(my_func)


# Note that these annotations do **not** force a type on the parameters or the return value - they are simply there for documentation purposes within Python and **may** be used by external applications and modules, such as IDE's.

# Just like docstrings are stored in the `__doc__` property, annotations are stored in the `__annotations__` property - a dictionary whose keys are the parameter names, and values are the annotation.

# In[13]:


my_func.__annotations__


# Of course we can combine both docstrings and annotations:

# In[14]:


def fact(n: 'int >= 0')->int:
    '''Calculates n! (factorial function)
    
    Inputs:
        n: non-negative integer
    Returns:
        the factorial of n
    '''
    
    if n < 0:
        '''Note that this is not part of the docstring!'''
        return 1
    else:
        return n * fact(n-1)


# In[15]:


help(fact)


# Annotations will work with default parameters too: just specify the default **after** the annotation:

# In[16]:


def my_func(a:str='a', b:int=1)->str:
    return a*b


# In[17]:


help(my_func)


# In[18]:


my_func()


# In[19]:


my_func('abc', 3)


# In[20]:


def my_func(a:int=0, *args:'additional args'):
    print(a, args)


# In[21]:


my_func.__annotations__


# In[22]:


help(my_func)

