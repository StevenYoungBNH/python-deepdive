#!/usr/bin/env python
# coding: utf-8

# ### Objects and Classes

# A class is a type of object. In Python we create classes using the `class` keyword.

# In[1]:


class Person:
    pass


# Now this class doesn't do much, but it is an object of type `type` (which is itself an object).

# In[2]:


type(Person)


# In[3]:


type(type)


# Classes have "built-in" attributes, even though we did not specifically add any to the class ourselves.
# 
# For example, they have a name:

# In[4]:


Person.__name__


# They are also callables, and calling a class results in the creation and return of a new **instance** of that class:

# In[5]:


p = Person()


# Now the type of the object is the class used to build that object:

# In[6]:


type(p)


# These instances also have "built_in" properties, which we will cover throughout this course.
# 
# For example, they have a `__class__` property that tells us which class was used to create the instance:

# In[7]:


p.__class__


# As you can see that returns the class object used to instantiate `p`.
# 
# In fact:

# In[8]:


type(p) is p.__class__


# We can also use `isinstance` to test if an object is an instance of a particular class - now this gets a bit more complicated when we use inheritance, but right now we're not, so it's quite straightforward:

# In[9]:


isinstance(p, Person)


# In[10]:


isinstance(p, str)


# We can even use `isinstance` with our class, since we know it's type is `type`:

# In[11]:


isinstance(Person, type)


# `type` is like the most generic kind of **class** object - we'll come back to this when discussing meta programming.
# 
# We really need inheritance to understand how this works, but every class **is** a `type` object (it inherits all the properties of `type`).
# 
# For now let's just see what functionality `type` has:

# In[12]:


help(type)


# As you can see it has a `__call__` method (that's how our class becomes callable), and a bunch of other attributes and methods that we'll see throughout this course.
# 
# Our class objects also have these properties, because they inherit from the `type` object.

# And in fact, `type` is an instance of itself - that's kind of weird, and not the case for our own classes:

# In[13]:


isinstance(type, type)


# In[14]:


isinstance(Person, Person)

