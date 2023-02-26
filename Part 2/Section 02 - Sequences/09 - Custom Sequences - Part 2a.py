#!/usr/bin/env python
# coding: utf-8

# ### Custom Sequences (Part 2a)

# We have seen before how we could define our own custom sequence type by implementing the `__len__` and `__getitem__` methods.
# 
# Here we are going to look at how to implement:
# * concatenation (`+`)
# * in-place concatenation (`+=`)
# * repetition (`*`)
# * in-place repetition (`*=`)
# * index assignment (`seq[i]=val`)
# * slice assignment (`seq[i:j]=iter` and `seq[i:j:k]=iter`)
# * append, extend, in, del, pop

# #### The `+` and `+=` Operators

# First we look at how we can overload the `+` and `+=` operators in a custom class in general. Then we'll look at how to use this in the context of sequences.

# We use the special functions `__add__` and `__iadd__`.
# 
# Just to see how those methods get called, we're actually going to implement them to just print out that they were called. As you can see, we can implement them however we want!

# In[1]:


class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'MyClass(name={self.name})'
    
    def __add__(self, other):
        print(f'You called + on {self} and {other}')
        return 'Hello from __add__'
        
    def __iadd__(self, other):
        print(f'You called += on {self} and {other}')
        return 'Hello from __iadd__'


# In[2]:


c1 = MyClass('instance 1')
c2 = MyClass('instance 2')


# In[3]:


c3 = c1 + c2


# In[4]:


c3


# In[5]:


c1 += c2


# In[6]:


c1


# Now let's tweak this code to make those operators concatenate the `name` property.
# 
# The thing to note is that when we add two objects together we generally expect them to be of the same type and to return an object of the same type (and in the case of `+=` it needs to return the original object).

# Let's quickly recall how those operators behave with lists:

# In[7]:


l1 = [1, 2, 3]
l2 = [4, 5, 6]
id(l1)


# In[8]:


l1 = l1 + l2
id(l1), l1


# Notice how the `id` of `l1` changed.

# But, with `+=`:

# In[9]:


l1 = [1, 2, 3]
l2 = [4, 5, 6]
id(l1)


# In[10]:


l1 += l2
id(l1), l1


# we can see that the concatenation results in the same elements, but this time the `id` of `l1` has not changed - an in-place operation took place.
# 
# Let's do something similar:

# In[11]:


class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'MyClass(name={self.name})'
    
    def __add__(self, other):
        return MyClass(self.name + ' ' + other.name)
        
    def __iadd__(self, other):
        self.name += ' ' + other.name
        return self
        


# In[12]:


c1 = MyClass('Eric')
c2 = MyClass('Idle')


# In[13]:


c3 = c1 + c2


# In[14]:


c3


# In[15]:


c1, c2


# In[16]:


c1 += c2


# In[17]:


c1


# #### The `*` and `*=` Operators

# Just as easily we can overload the `*` and `*=` operators too, using the `__mul__` and `__imul__` methods.

# In[18]:


class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'MyClass(name={self.name})'
    
    def __add__(self, other):
        return MyClass(self.name + ' ' + other.name)
        
    def __iadd__(self, other):
        self.name += ' ' + other.name
        return self
    
    def __mul__(self, n):
        return MyClass(self.name * n)
        
    def __imul__(self, n):
        self.name *= n
        return self


# In[19]:


c1 = MyClass('Eric')


# In[20]:


c1 * 3


# In[21]:


c1


# In[22]:


c1 *= 4 


# In[23]:


c1


# And if we try something not supported:

# In[24]:


c1 = MyClass('Eric')
c1 * 'hello'


# As you can see, we get the correct exception - and we didn't even have to guard against that exception and raise our own error. Since we delegated our `*` call to multiplying a sequence by something else, we could simply let Python handle any exceptions.
# 
# We'll actually get into a lot of detail with exception handling later in this course.

# What about multiplying an integer by the sequence?

# In[25]:


c1 = MyClass('Monty')
2 * c1


# To handle this we need to implement the `__rmul__` method:

# In[26]:


class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'MyClass(name={self.name})'
    
    def __add__(self, other):
        return MyClass(self.name + ' ' + other.name)
        
    def __iadd__(self, other):
        self.name += ' ' + other.name
        return self
    
    def __mul__(self, n):
        return MyClass(self.name * n)
        
    def __imul__(self, n):
        self.name *= n
        return self
    
    def __rmul__(self, n):
        self.name *= n
        return self


# In[27]:


c1 = MyClass('Monty')


# In[28]:


2 * c1


# #### Implementing the `in` operator

# For this example, we'll want `in` to test if the something is contained in the name string of our class:

# In[29]:


class MyClass:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'MyClass(name={self.name})'
    
    def __add__(self, other):
        return MyClass(self.name + ' ' + other.name)
        
    def __iadd__(self, other):
        self.name += ' ' + other.name
        return self
    
    def __mul__(self, n):
        return MyClass(self.name * n)
        
    def __imul__(self, n):
        self.name *= n
        return self
    
    def __rmul__(self, n):
        self.name *= n
        return self
    
    def __contains__(self, value):
        return value in self.name


# In[30]:


c1 = MyClass('MontyPython')


# In[31]:


'ty' in c1

