#!/usr/bin/env python
# coding: utf-8

# ### `__str__` and `__repr__`

# Let's see how this works by first implementing the `__repr__` method:

# In[1]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        print('__repr__ called')
        return f"Person(name='{self.name}, age={self.age}')"


# In[2]:


p = Person('Python', 30)


# Here's how Jupyter shows us the string representation for the object `p`:

# In[3]:


p


# Here's what it looks like when we use the `print` function:

# In[4]:


print(p)


# Here's what happens if we call the `repr` function:

# In[5]:


repr(p)


# And here's what happens when we call the `str` function:

# In[6]:


str(p)


# As you can see, in all cases, our `__repr__` method was called.
# 
# Now, let's implement a `__str__` method:

# In[7]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        print('__repr__ called')
        return f"Person(name='{self.name}, age=self.age')"
    
    def __str__(self):
        print('__str__ called')
        return self.name


# In[8]:


p = Person('Python', 30)


# And let's try out each of the ways to get a string representation for `p`:

# In[9]:


p


# So, same as before - uses the `__repr__` method.

# In[10]:


print(p)


# As you can see, `print` will try to use `__str__` if present, otherwise it will fall back to using `__repr__`.

# In[11]:


str(p)


# As expected, `str()` will try to use the `__str__` method first.

# In[12]:


repr(p)


# Whereas the `repr()` method will use the `__repr__` method directly.

# What happens if we define a `__str__` method, but not `__repr__` method.
# 
# We'll look at inheritance later, but for now think of it as Python providing "defaults" for those methods when they are not present.
# 
# Let's first see how it works if we do not have either of those methods for two different classes:

# In[13]:


class Person:
    pass

class Point:
    pass


# In[14]:


person = Person()
point = Point()


# In[15]:


repr(person), repr(point)


# As we can see, Python provides a default representation for objects that contains the class name, and the instance memory address.
# 
# If we use `str()` instead, we get the same result:

# In[16]:


str(person), str(point)


# Now let's go back to our original `Person` class and remove the `__repr__` method:

# In[17]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        print('__str__ called')
        return self.name


# In[18]:


p = Person('Python', 30)


# In[19]:


p


# In[20]:


repr(p)


# Since we do not have a `__repr__` method, Python uses the "default" - it does not use our custom `__str__` method!

# But if we use `print()` or `str()`:

# In[21]:


print(p)


# In[22]:


str(p)


# Lastly, various formatting functions will also prefer using the `__str__` method when available. Lert's first go back to our `Person` class that implements both:

# In[23]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        print('__repr__ called')
        return f"Person(name='{self.name}, age=self.age')"
    
    def __str__(self):
        print('__str__ called')
        return self.name


# In[24]:


p = Person('Python', 30)


# In[25]:


f'The person is {p}'


# In[26]:


'The person is {}'.format(p)


# In[27]:


'The person is %s' % p


# In[ ]:




