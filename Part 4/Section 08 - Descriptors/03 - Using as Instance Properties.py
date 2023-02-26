#!/usr/bin/env python
# coding: utf-8

# ### Using as Instance Properties

# So let's start exploring how we can use descriptors to read and write instance properties.

# We might try something like this first:

# In[1]:


class IntegerValue:
    def __set__(self, instance, value):
        instance.stored_value = int(value)
        
    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return getattr(instance, 'stored_value', None)


# Basically we are going to use the instance dictionary to store the value under some name (symbol) in it - what name should we use? That could be an issue, and we'll come back to that.

# In[2]:


class Point1D:
    x = IntegerValue()


# In[3]:


p1, p2 = Point1D(), Point1D()


# In[4]:


p1.x = 10.1
p2.x = 20.2


# In[5]:


p1.x, p2.x


# As you can see, we now have a descriptor that uses the instances themselves to store the data:

# In[6]:


p1.__dict__, p2.__dict__


# But you'll notice that our descriptor is hard coded to using the same key in the instance dictionaries - which leads us to this problem:

# In[7]:


class Point2D:
    x = IntegerValue()
    y = IntegerValue()


# In[8]:


p = Point2D()


# In[9]:


p.x = 10.1


# In[10]:


p.__dict__


# And what happens if we set `y`? What symbol is the descriptor going to use to store the value in the instance?

# In[11]:


p.y = 20.2


# In[12]:


p.__dict__


# Yep, the **same** symbol!

# In[13]:


p.x, p.y


# So that appropach is not going to work either. Somehow we would need to have a distinct storage name for each property.
# 
# We could do this by using the `__init__` of our descriptor:

# In[14]:


class IntegerValue:
    def __init__(self, name):
        self.storage_name = '_' + name 
        
    def __set__(self, instance, value):
        setattr(instance, self.storage_name, int(value))
        
    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return getattr(instance, self._storage_name, None)
        
class Point2D:
    x = IntegerValue('x')
    y = IntegerValue('y')


# In[15]:


p1 = Point2D()
p2 = Point2D()


# In[16]:


p1.x = 10.1
p1.y = 20.2


# In[17]:


p1.__dict__


# In[18]:


p2.x = 100.1
p2.y = 200.2


# In[19]:


p2.__dict__


# So this approach can work just fine, but there are a few drawbacks:
# 
# 1. The user needs to specify the name of the property twice
# 2. We assume that `_` + `name` is not also used by the class in which the descriptor exists (so that could be a major problem)
# 3. We assume we can add an attribute to the instance - but what if it uses slots?

# One way we could get around each of those problems is by using the descriptor instance itself to store the instance values. But as we saw earlier, we can't just set an attribute in the descriptor instance, since that would be shared across multiple instances of the class containing the descriptor.
# 
# Instead, we are going to **assume** that the `instance` is a hashable object, and use a dictionary in the descriptor to store instance specific values:

# In[20]:


class IntegerValue:
    def __init__(self):
        self.values = {}
        
    def __set__(self, instance, value):
        self.values[instance] = int(value)
        
    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return self.values.get(instance)


# In[21]:


class Point2D:
    x = IntegerValue()
    y = IntegerValue()


# In[22]:


p1 = Point2D()
p2 = Point2D()


# In[23]:


p1.x = 10.1
p1.y = 20.2


# In[24]:


p1.x, p1.y


# In fact, we can see the dictionary in the descriptor instances:

# In[25]:


Point2D.x.values


# In[26]:


Point2D.x.values


# where the key in both of these is our `p1` object:

# In[27]:


hex(id(p1))


# We can now create a second point, and go through the same steps:

# In[28]:


p2 = Point2D()
p2.x = 100.1
p2.y = 200.2


# In[29]:


hex(id(p2))


# In[30]:


Point2D.x.values


# In[31]:


Point2D.y.values


# And everything works just fine:

# In[32]:


p1.x, p1.y, p2.x, p2.y


# Or does it??

# We actually have a potential memory leak - notice how the dictionary in the desccriptor instance is **also** storing a reference to the point object - as a **key** in the dictionary.

# Let's write a simple utility function that allows us to get the reference count for an object given it's id (and it only makes sense if the id we use still has a valid non-destroyed object):

# In[33]:


import ctypes

def ref_count(address):
    return ctypes.c_long.from_address(address).value


# In[34]:


p1 = Point2D()
id_p1 = id(p1)


# In[35]:


ref_count(id_p1)


# Now let's set the `x` property of `p1`:

# In[36]:


p1.x = 100.1


# And let's check the ref count again:

# In[37]:


ref_count(id_p1)


# As you can see it's now `2`. if we delete our main reference to `p1` that is in our global namespace:

# In[38]:


'p1' in globals()


# In[39]:


del p1


# In[40]:


'p1' in globals()


# In[41]:


ref_count(id_p1)


# And our reference count is still `1`, which means the object itself has not been destroyed!

# In fact, we can see that object referenced in our data descriptor dictionary:

# In[42]:


Point2D.x.values.items()


# In[43]:


hex(id_p1)


# As you can see, the last element's key is the same id as what `p1` was referencing.

# So, although we deleted `p1`, the object was not destroyed - this can result in a memory leak.

# There are a few ways we can handle this issue. The first one we are going to look at is something called **weak references**. So let's segway into that next.
