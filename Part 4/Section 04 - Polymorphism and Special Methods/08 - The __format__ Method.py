#!/usr/bin/env python
# coding: utf-8

# ### The `__format__` Method

# We saw before the use of `__str__` and `__repr__`.

# However we have one more formatting function to look at!
# 
# The `format()` function.

# For example we can use `format()` with a format specification for floats:

# In[1]:


a = 0.1


# In[2]:


format(a, '.20f')


# Or we can use it with a datetime object:

# In[3]:


from datetime import datetime


# In[4]:


now = datetime.utcnow()


# In[5]:


now


# In[6]:


format(now, '%a %Y-%m-%d  %I:%M %p')


# We can implement support for format specifiers in our own classes by implementing the `__format__` method.
# 
# This is actually quite complicated to do, so we usually delegate back to some other type's formatting.
# 
# Just like with `__str__` and `__repr__`, `__format__` should return a string.

# In[7]:


class Person:
    def __init__(self, name, dob):
        self.name = name
        self.dob = dob
        
    def __repr__(self):
        print('__repr__ called...')
        return f'Person(name={self.name}, dob={self.dob.isoformat()})'
    
    def __str__(self):
        print('__str__ called...')
        return f'Person({self.name})'
    
    def __format__(self, date_format_spec):
        print(f'__format__ called with {repr(date_format_spec)}...')
        dob = format(self.dob, date_format_spec)
        return f'Person(name={self.name}, dob={dob})'


# So now have:

# In[8]:


from datetime import date

p = Person('Alex', date(1900, 10, 20))


# In[9]:


str(p)


# In[10]:


repr(p)


# In[11]:


format(p, '%B %d, %Y')


# If we do not specify a format, then the `format` function will use an empty string:

# In[12]:


format(p)

