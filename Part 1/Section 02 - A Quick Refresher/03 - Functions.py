#!/usr/bin/env python
# coding: utf-8

# ### Functions

# Python has many built-in functions and methods we can use

# Some are available by default:

# In[1]:


s = [1, 2, 3]
len(s)


# While some need to be imported:

# In[2]:


from math import sqrt


# In[3]:


sqrt(4)


# Entire modules can be imported:

# In[4]:


import math


# In[5]:


math.exp(1)


# We can define our own functions:

# In[8]:


def func_1():
    print('running func1')


# In[9]:


func_1()


# Note that to "call" or "invoke" a function we need to use the **()**.
# 
# Simply using the function name without the **()** refers to the function, but does not call it:

# In[11]:


func_1


# We can also define functions that take parameters:

# In[12]:


def func_2(a, b):
    return a * b


# Note that **a** and **b** can be any type (this is an example of polymorphism - which we will look into more detail later in this course). 
# 
# But the function will fail to run if **a** and **b** are types that are not "compatible" with the ***** operator:

# In[13]:


func_2(3, 2)


# In[14]:


func_2('a', 3)


# In[15]:


func_2([1, 2, 3], 2)


# In[16]:


func_2('a', 'b')


# It is possible to use **type annotations**:

# In[17]:


def func_3(a: int, b:int):
    return a * b


# In[18]:


func_3(2, 3)


# In[19]:


func_3('a', 2)


# But as you can see, these do not enforce a data type! They are simply metadata that can be used by external libraries, and many IDE's.

# Functions are objects, just like integers are objects, and they can be assigned to variables just as an integer can:

# In[20]:


my_func = func_3


# In[21]:


my_func('a', 2)


# Functions **must** always return something. If you do not specify a return value, Python will automatically return the **None** object:

# In[22]:


def func_4():
    # does something but does not return a value
    a = 2


# In[23]:


res = func_4()


# In[24]:


print(res)


# The **def** keyword is an executable piece of code that creates the function (an instance of the **function** class) and essentially assigns it to a variable name (the function **name**). 
# 
# Note that the function is defined when **def** is reached, but the code inside it is not evaluated until the function is called.
# 
# This is why we can define functions that call other functions defined later - as long as we don't call them before all the necessary functions are defined.

# For example, the following will work:

# In[31]:


def fn_1():
    fn_2()
    
def fn_2():
    print('Hello')
    
fn_1()


# But this will not work:

# In[32]:


def fn_3():
    fn_4()

fn_3()

def fn_4():
    print('Hello')


# We also have the **lambda** keyword, that also creates a new function, but does not assign it to any specific name - instead it just returns the function object - which we can, if we wish, assign to a variable ourselves:

# In[28]:


func_5 = lambda x: x**2


# In[29]:


func_5


# In[30]:


func_5(2)


# We'll examine lambdas in more detail later in this course.
