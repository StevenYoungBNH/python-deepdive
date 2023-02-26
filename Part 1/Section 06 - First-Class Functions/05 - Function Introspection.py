#!/usr/bin/env python
# coding: utf-8

# ### Function Introspection

# In[1]:


def fact(n: "some non-negative integer") -> "n! or 0 if n < 0":
    """Calculates the factorial of a non-negative integer n
    
    If n is negative, returns 0.
    """
    if n < 0:
        return 0
    elif n <= 1:
        return 1
    else:
        return n * fact(n-1)


# Since functions are objects, we can add attributes to a function:

# In[2]:


fact.short_description = "factorial function"


# In[3]:


print(fact.short_description)


# We can see all the attributes that belong to a function using the **dir** function:

# In[4]:


dir(fact)


# We can see our **short_description** attribute, as well as some attributes we have seen before: **__annotations__** and **__doc__**:

# In[5]:


fact.__doc__


# In[6]:


fact.__annotations__


# We'll revisit some of these attributes later in this course, but let's take a look at a few here:

# In[7]:


def my_func(a, b=2, c=3, *, kw1, kw2=2, **kwargs):
    pass


# Let's assign my_func to another variable:

# In[8]:


f = my_func


# The **__name__** attribute holds the function's name:

# In[9]:


my_func.__name__


# In[10]:


f.__name__


# The **__defaults__** attribute is a tuple containing any positional parameter defaults:

# In[11]:


my_func.__defaults__


# In[12]:


my_func.__kwdefaults__


# Let's create a function with some local variables:

# In[13]:


def my_func(a, b=1, *args, **kwargs):
    i = 10
    b = min(i, b)
    return a * b


# In[14]:


my_func('a', 100)


# The **__code__** attribute contains a **code** object:

# In[15]:


my_func.__code__


# This **code** object itself has various properties:

# In[16]:


dir(my_func.__code__)


# Attribute **__co_varnames__** is a tuple containing the parameter names and local variables:

# In[17]:


my_func.__code__.co_varnames


# Attribute **co_argcount** returns the number of arguments (minus any \* and \*\* args)

# In[18]:


my_func.__code__.co_argcount


# #### The **inspect** module

# It is much easier to use the **inspect** module!

# In[19]:


import inspect


# In[20]:


inspect.isfunction(my_func)


# By the way, there is a difference between a function and a method! A method is a function that is bound to some object:

# In[21]:


inspect.ismethod(my_func)


# In[22]:


class MyClass:
    def f_instance(self):
        pass
    
    @classmethod
    def f_class(cls):
        pass
    
    @staticmethod
    def f_static():
        pass


# **Instance methods** are bound to the **instance** of a class (not the class itself)

# **Class methods** are bound to the **class**, not instances

# **Static methods** are no bound either to the class or its instances

# In[23]:


inspect.isfunction(MyClass.f_instance), inspect.ismethod(MyClass.f_instance)


# In[24]:


inspect.isfunction(MyClass.f_class), inspect.ismethod(MyClass.f_class)


# In[25]:


inspect.isfunction(MyClass.f_static), inspect.ismethod(MyClass.f_static)


# In[26]:


my_obj = MyClass()


# In[27]:


inspect.isfunction(my_obj.f_instance), inspect.ismethod(my_obj.f_instance)


# In[28]:


inspect.isfunction(my_obj.f_class), inspect.ismethod(my_obj.f_class)


# In[29]:


inspect.isfunction(my_obj.f_static), inspect.ismethod(my_obj.f_static)


# If you just want to know if something is a function or method:

# In[30]:


inspect.isroutine(my_func)


# In[31]:


inspect.isroutine(MyClass.f_instance)


# In[32]:


inspect.isroutine(my_obj.f_class)


# In[33]:


inspect.isroutine(my_obj.f_static)


# We'll revisit this in more detail in section on OOP.

# #### Introspecting Callable Code

# We can get back the source code of our function using the **getsource()** method:

# In[34]:


inspect.getsource(fact)


# In[35]:


print(inspect.getsource(fact))


# In[36]:


inspect.getsource(MyClass.f_instance)


# In[37]:


inspect.getsource(my_obj.f_instance)


# We can also find out where the function was defined:

# In[38]:


inspect.getmodule(fact)


# In[39]:


inspect.getmodule(print)


# In[40]:


import math


# In[41]:


inspect.getmodule(math.sin)


# In[42]:


# setting up variable
i = 10

# comment line 1
# comment line 2
def my_func(a, b=1):
    # comment inside my_func
    pass


# In[43]:


inspect.getcomments(my_func)


# In[44]:


print(inspect.getcomments(my_func))


# #### Introspecting Callable Signatures

# In[45]:


# TODO: Provide implementation
def my_func(a: 'a string', 
            b: int = 1, 
            *args: 'additional positional args', 
            kw1: 'first keyword-only arg', 
            kw2: 'second keyword-only arg' = 10,
            **kwargs: 'additional keyword-only args') -> str:
    """does something
       or other"""
    pass


# In[46]:


inspect.signature(my_func)


# In[47]:


type(inspect.signature(my_func))


# In[48]:


sig = inspect.signature(my_func)


# In[49]:


dir(sig)


# In[50]:


for param_name, param in sig.parameters.items():
    print(param_name, param)


# In[51]:


def print_info(f: "callable") -> None:
    print(f.__name__)
    print('=' * len(f.__name__), end='\n\n')
    
    print('{0}\n{1}\n'.format(inspect.getcomments(f), 
                              inspect.cleandoc(f.__doc__)))
    
    print('{0}\n{1}'.format('Inputs', '-'*len('Inputs')))
    
    sig = inspect.signature(f)
    for param in sig.parameters.values():
        print('Name:', param.name)
        print('Default:', param.default)
        print('Annotation:', param.annotation)
        print('Kind:', param.kind)
        print('--------------------------\n')
        
    print('{0}\n{1}'.format('\n\nOutput', '-'*len('Output')))
    print(sig.return_annotation)


# In[52]:


print_info(my_func)


# #### A Side Note on Positional Only Arguments

# Some built-in callables have arguments that are positional only (i.e. cannot be specified using a keyword).
# 
# However, Python does not currently have any syntax that allows us to define callables with positional only arguments.
# 
# In general, the documentation uses a **/** character to indicate that all preceding arguments are positional-only. But not always :-(

# In[53]:


help(divmod)


# Here we see that the **divmod** function takes two positional-only parameters:

# In[54]:


divmod(10, 3)


# In[55]:


divmod(x=10, y=3)


# Similarly, the string **replace** function also takes positional-only arguments, however, the documentation does not indicate this!

# In[56]:


help(str.replace)


# In[57]:


'abcdefg'.replace('abc', 'xyz')


# In[58]:


'abcdefg'.replace(old='abc', new='xyz')

