#!/usr/bin/env python
# coding: utf-8

# ### Booleans

# As we know every object in Python has an associated truth value. Empty container types are falsy, non-zero numbers are truthy, zero numbers are falsy, etc.

# The way Python determines the truth value of our custom classes is to:
# 1. first look for an implementation of the `__bool__` method (which needs to return a boolean)
# 2. if not present, looks for `__len__` and will return `False` if that is `0`, and `True` otherwise
# 3. otherwise returns `True`

# Let's look at some example which illustrate this behavior:

# First let's not define anything, so our objects should always have a `True` associated truth value:

# In[1]:


class Person:
    pass


# In[2]:


p = Person()


# In[3]:


bool(p)


# Now let's implement the `__len__` method:

# In[4]:


class MyList:
    def __init__(self, length):
        self._length = length
        
    def __len__(self):
        print('__len__ called')
        return self._length


# In[5]:


l1 = MyList(0)  # so __len__ will return 0
l2 = MyList(10)  # so __len__ will return 10


# In[6]:


bool(l1)


# In[7]:


bool(l2)


# So when we create custom iterables, as long as we have a `__len__` method implemented, we can actually skip implementing the `__bool__` method, and our class will remain consistent with other collection types behaviors (empty collections are falsy, otherwise truthy).

# Let's implement the `__bool__` method though, just to see that if it is present it will get called instead of the `__len__` method:

# In[8]:


class MyList:
    def __init__(self, length):
        self._length = length
        
    def __len__(self):
        print('__len__ called')
        return self._length
    
    def __bool__(self):
        print('__bool__ called')
        return self._length > 0


# In[9]:


p1 = MyList(0)
p2 = MyList(100)


# In[10]:


bool(p1)


# In[11]:


bool(p2)


# For classes that do not define `__len__` we may want to use the `__bool__` method. For example, consider a 2D `Point` class where we want to consider the origin point `(0,0)` falsy, and everything else truthy.
# 
# By default, all instances of our `Point` class will be truthy (they have neither a `__len__` nor a `__bool__` method):

# In[12]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# In[13]:


p1 = Point(0, 0)
p2 = Point(1, 1)


# In[14]:


bool(p1), bool(p2)


# So now let's implement `__bool__` to get our desired functionality:

# In[15]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __bool__(self):
        return self.x != 0 or self.y != 0


# In[16]:


p1 = Point(0, 0)
p2 = Point(1, 1)


# In[17]:


bool(p1)


# In[18]:


bool(p2)


# Note that with associated values, we could technically do something like this:

# In[19]:


bool(p1.x or p1.y)


# In[20]:


bool(p2.x or p2.y)


# This works because any `0` number is falsy.
# 
# So we might think we can use this approach instead of the explicit `!= 0` comparisons:

# In[21]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __bool__(self):
        return self.x or self.y


# In[22]:


p1 = Point(0, 0)
p2 = Point(1, 1)


# Then if we call `__bool__` directly:

# In[23]:


bool(p1.__bool__()), bool(p2.__bool__())


# But it we try to use the `bool()` function:

# In[24]:


try:
    bool(p1)
except TypeError as ex:
    print(ex)


# we can see that we have an exception. Although we can work with truth values in most circumstances, Python insists that `__bool__` should return an actual boolean type.

# If we really wanted to, we could write:

# In[25]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __bool__(self):
        return bool(self.x or self.y)


# In[26]:


p1 = Point(0, 0)
p2 = Point(1, 1)


# In[27]:


bool(p1), bool(p2)


# In[ ]:




