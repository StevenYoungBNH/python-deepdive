#!/usr/bin/env python
# coding: utf-8

# ### Reducing Functions in Python

# #### Maximum and Minimum

# Suppose we want to find the maximum value in a list:

# In[1]:


l = [5, 8, 6, 10, 9]


# We can solve this problem using a **for** loop.

# First we define a function that returns the maximum of two arguments:

# In[2]:


_max = lambda a, b: a if a > b else b


# In[3]:


def max_sequence(sequence):
    result = sequence[0]
    for x in sequence[1:]:
        result = _max(result, x)
    return result


# In[4]:


max_sequence(l)


# To calculate the minimum, all we need to do is to change the function that is repeatedly applied:

# In[5]:


_min = lambda a, b: a if a < b else b


# In[6]:


def min_sequence(sequence):
    result = sequence[0]
    for x in sequence[1:]:
        result = _min(result, x)
    return result


# In[7]:


print(l)
print(min_sequence(l))


# In general we could write it like this:

# In[8]:


def _reduce(fn, sequence):
    result = sequence[0]
    for x in sequence[1:]:
        result = fn(result, x)
    return result


# In[9]:


_reduce(_max, l)


# In[10]:


_reduce(_min, l)


# We could even just use a lambda directly in the call to **\_reduce**:

# In[11]:


_reduce(lambda a, b: a if a > b else b, l)


# In[12]:


_reduce(lambda a, b: a if a < b else b, l)


# Using the same approach, we could even add all the elements of a sequence together:

# In[13]:


print(l)


# In[14]:


_reduce(lambda a, b: a + b, l)


# Python actually implements a reduce function, which is found in the **functools** module. Unlike our **\_reduce** function, it can handle any iterable, not just sequences.

# In[15]:


from functools import reduce


# In[16]:


l


# In[17]:


reduce(lambda a, b: a if a > b else b, l)


# In[18]:


reduce(lambda a, b: a if a < b else b, l)


# In[19]:


reduce(lambda a, b: a + b, l)


# Finding the max and min of an iterable is such a common thing that Python provides a built-in function to do just that:

# In[20]:


max(l), min(l)


# Finding the sum of all the elements in an iterable is also common enough that Python implements the **sum** function:

# In[21]:


sum(l)


# #### The **any** and **all** built-ins

# Python provides two additional built-in reducing functions: **any** and **all**.

# The **any** function will return **True** if any element in the iterable is truthy:

# In[22]:


l = [0, 1, 2]
any(l)


# In[23]:


l = [0, 0, 0]
any(l)


# On the other hand, **all** will return True if **every** element of the iterable is truthy:

# In[24]:


l = [0, 1, 2]
all(l)


# In[25]:


l = [1, 2, 3]
all(l)


# We can implement these functions ourselves using **reduce** if we choose to - simply use the Boolean **or** or **and** operators as the function passed to **reduce** to implement **any** and **all** respectively.

# #### any

# In[26]:


l = [0, 1, 2]
reduce(lambda a, b: bool(a or b), l)


# In[27]:


l = [0, 0, 0]
reduce(lambda a, b: bool(a or b), l)


# #### all

# In[28]:


l = [0, 1, 2]
reduce(lambda a, b: bool(a and b), l)


# In[29]:


l = [1, 2, 3]
reduce(lambda a, b: bool(a and b), l)


# #### Products

# Sometimes we may want to find the product of every element of an iterable.
# 
# Python does not provide us a built-in method to do this, so we have to either use a procedural approach, or we can use the **reduce** function.

# We start by defining a function that multiplies two arguments together:

# In[30]:


def mult(a, b):
    return a * b


# Then we can use the **reduce** function:

# In[31]:


l = [2, 3, 4]
reduce(mult, l)


# Remember what this did:
# 
#     step 1: result = 2
#     step 2: result = mult(result, 3) = mult(2, 3) = 6
#     step 3: result = mult(result, 4) = mult(6, 4) = 24
#     step 4: l exhausted, return result --> 24

# Of course, we can also just use a lambda:

# In[32]:


reduce(lambda a, b: a * b, l)


# #### Factorials

# ##### Factorials

# A special case of the product we just did would be calculating the factorial of some number (**n!**):

# Recall:
# 
#     n! = 1 * 2 * 3 * ... * n

# In other words, we are calculating the product of a sequence containing consecutive integers from 1 to n (inclusive)

# We can easily write this using a simple for loop:

# In[33]:


def fact(n):
    if n <= 1:
        return 1
    else:
        result = 1
        for i in range(2, n+1):
            result *= i
        return result


# In[34]:


fact(1), fact(2), fact(3), fact(4), fact(5)


# We could also write this using a recursive function:

# In[35]:


def fact(n):
    if n <=1:
        return 1
    else:
        return n * fact(n-1)


# In[36]:


fact(1), fact(2), fact(3), fact(4), fact(5)


# Finally we can also write this using **reduce** as follows:

# In[37]:


n = 5
reduce(lambda a, b: a * b, range(1, n+1))


# As you can see, the **reduce** approach, although concise, is sometimes more difficult to understand than the plain loop or recursive approach.

# #### **reduce** initializer

# Suppose we want to provide some sort of default when we claculate the product of the elements of an iterable if that iterable is empty:

# In[38]:


l = [1, 2, 3]
reduce(lambda x, y: x*y, l)


# but if **l** is empty:

# In[39]:


l = []
reduce(lambda x, y: x*y, l)


# To fix this, we can provide an initializer. In this case, we will use **1** since that will not affect the result of the product, and still allow us to return a value for an empty iterable.

# In[40]:


l = []
reduce(lambda x, y: x*y, l, 1)


# In[ ]:




