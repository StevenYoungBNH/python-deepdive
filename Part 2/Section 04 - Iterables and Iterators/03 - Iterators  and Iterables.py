#!/usr/bin/env python
# coding: utf-8

# ### Iterators and Iterables

# Previously we saw that we could create **iterator** objects by simply implementing:
# 
# * a `__next__` method that returns the next element in the container
# * an `__iter__` method that just returns the object itself (the iterator object)

# Doing that we could use a `for` loop, list comprehensions, and in fact use that iterator object anywhere an iterable was expected (like `enumerate`, `sorted`, and so on).

# However, we had two outstanding issues/questions:
# * when we looped over the iterator using a `for` loop (or a comprehension, or other functions that do some form of iteration), we saw that the `__iter__` was always called first.
# * the iterator gets exhausted after we have finished iterating it fully - which means we have to create a new iterator every time we want to use a new iteration over the collection - can we somehow avoid having to remember to do that every time?

# The answer to both of these questions are related.

# Let's start by looking at how we might avoid having to create a new instance of the collection every time we want to iterate over it.
# 
# After all, we don't need a new instance of the elements, just some kind of *resetting* of *current* item.

# Let's start with a simple example that has those issues:

# In[1]:


class Cities:
    def __init__(self):
        self._cities = ['Paris', 'Berlin', 'Rome', 'Madrid', 'London']
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        else:
            item = self._cities[self._index]
            self._index += 1
            return item


# Now, we have an **iterator** object, but we need to re-create it every time we want to start the iterations from the beginning:

# In[2]:


cities = Cities()
list(enumerate(cities))


# In[3]:


cities = Cities()
[item.upper() for item in cities]


# In[4]:


cities = Cities()
sorted(cities)


# So, we basically have to "restart" an iterator by **creating a new one each time**.

# But in this case, we are also re-creating the underlying data every time - seems wasteful!

# Instead, maybe we can split the **iterator** part of our code from the **data** part of our code.

# In[5]:


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)


# And let's create our iterator this way:

# In[6]:


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        self._city_obj = city_obj
        self._index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


# So now we can create our `Cities` instance **once**:

# In[7]:


cities = Cities()


# and create as many iterators as we want, but passing it the same `Cities` instance everyt time:

# In[8]:


iter_1 = CityIterator(cities)


# In[9]:


for city in iter_1:
    print(city)


# In[10]:


iter_2 = CityIterator(cities)
[city.upper() for city in iter_2]


# So, we're almost at a solution now. At least we can create the **iterator** objects without having to recreate the `Cities` object every time.
# 
# But, we still have to remember to create a new iterator, **and** we can no longer iterate over the `cities` object anymore!

# In[11]:


for city in cities:
    print(city)


# This is where the first question we asked comes into play. Whenever we iterated our iterator, the first thing Python did was call `__iter__`.

# In fact, let's just check that again:

# In[12]:


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0
        
    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self
    
    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


# In[13]:


iter_1 = CityIterator(cities)


# In[14]:


for city in iter_1:
    print(city)


# #### Iterables

# Now we finally come to how an **iterable** is defined in Python.
# 
# An **iterable** is an object that:
# * implements the `__iter__` method
# * and that method returns an **iterator** which can be used to iterate over the object

# What would happen if we put an `__iter__` method in the `Cities` object and then try to iterate?
# 
# When we try to iterate over the `Cities` instance, Python will first call `__iter__`. The `__iter__` method should then return an **iterator** which Python will use for the iteration.
# 
# We actually have everything we need to now make `Cities` an **iterable** since we already have the `CityIterator` created:

# In[15]:


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0
        
    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self
    
    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


# In[16]:


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
    
    def __iter__(self):
        print('Calling Cities instance __iter__')
        return CityIterator(self)


# In[17]:


cities = Cities()


# In[18]:


for city in cities:
    print(city)


# And watch what happens if we try to run that loop again:

# In[19]:


for city in cities:
    print(city)


# A new **iterator** was created when the `for` loop started.
# 
# In fact, same happens for anything that is going to iterate our iterable - it first calls the `__iter__` method of the itrable to get a **new** iterator, then uses the iterator to call `__next__`.

# In[20]:


list(enumerate(cities))


# In[21]:


sorted(cities, reverse=True)


# Now we can put the iterator class inside our `Cities` class to keep the code self-contained:

# In[22]:


del CityIterator  # just to make sure CityIterator is not in our global scope


# In[23]:


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
    
    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)
    
    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item


# In[24]:


cities = Cities()


# In[25]:


list(enumerate(cities))


# Technically we can even get an iterator instance ourselves directly, by calling `iter()` on the `cities` object:

# In[26]:


iter_1 = iter(cities)
iter_2 = iter(cities)


# As you can see, Python created and returned two different instances of the `CityIterator` object.

# In[27]:


id(iter_1), id(iter_2)


# And now we also have should understand why **iterators** also implement the `__iter__` method (that just returns themselves) - it makes them **iterables** too!

# #### Mixing Iterables and Sequences

# `Cities` is an iterable, but it is not a sequence type:

# In[28]:


cities = Cities()


# In[29]:


len(cities)


# In[30]:


cities[1]


# Since our Cities **could** also be a sequence, we could also decide to implement the `__getitem__` method to make it into a sequence:

# In[31]:


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
    
    def __getitem__(self, s):
        print('getting item...')
        return self._cities[s]
    
    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)
    
    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item


# In[32]:


cities = Cities()


# It's a sequence:

# In[33]:


cities[0]


# It's also an iterable:

# In[34]:


next(iter(cities))


# Now that Cities is both a sequence type (`__getitem__`) and an iterable (`__iter__`), when we loop over `cities`, is Python going to use `__getitem__` or `__iter__`?

# In[35]:


cities = Cities()
for city in cities:
    print(city)


# It uses the iterator - so Python will use the iterator if there is one, otherwise it will fall back to using `__getitem__`. If neither is implemented, we'll get an exception.
# 
# Of course, for selection by index or slice, the `__getitem__` method **must** be implemented.
# 
# We'll come back to this very topic in an upcoming video, because behind the scenes, even if we only implement the `__getitem__` method, Python will auto-generate an iterator for us!

# ### Python Built-In Iterables and Iterators

# The way iterables and iterators work in our custom `Cities` example is exactly the way Python iterables work too.

# In[36]:


l = [1, 2, 3]


# Since lists are iterables, they implement the `__iter__` method and we can get an **iterator** for the list:

# In[37]:


iter_l = iter(l)
#or could use iter_1 = l.__iter__()


# In[38]:


type(iter_l)


# In[39]:


next(iter_l)


# In[40]:


next(iter_l)


# In[41]:


next(iter_l)


# In[42]:


next(iter_l)


# See? The same `StopIteration` exception is raised.
# 
# Since `iter_l` is an iterator, it also implements the `__iter__` method, which just returns the iterator itself:

# In[43]:


id(iter_l), id(iter(iter_l))


# In[44]:


'__next__' in dir(iter_l)


# In[45]:


'__iter__' in dir(iter_l)


# Since the list `l` is an iterable it also implements the `__iter__` method:

# In[46]:


'__iter__' in dir(l)


# but does not implement a `__next__` method:

# In[47]:


'__next__' in dir(l)


# Of course, since lists are also sequence types, they also implement the `__getitem__` method:

# In[48]:


'__getitem__' in dir(l)


# Sets and dictionaries on the other hand are not sequence types:

# In[49]:


'__getitem__' in dir(set)


# In[50]:


'__iter__' in dir(set)


# In[51]:


s = {1, 2, 3}
'__next__' in dir(iter(s))


# In[52]:


'__iter__' in dir(dict)


# But what does the iterator for a dictionary actually return? It iterates over what? You should probably already guess the answer to that one!

# In[53]:


d = dict(a=1, b=2, c=3)


# In[54]:


iter_d = iter(d)


# In[55]:


next(iter_d)


# Dictionary iterators will iterate over the **keys** of the dictionary.

# To iterate over the values, we could use the `values()` method which returns an **iterable** over the values of the dictionary:

# In[56]:


iter_vals = iter(d.values())


# In[57]:


next(iter_vals)


# And to iterate over both the keys and values, dictionaries provide an `items()` iterable:

# In[58]:


iter_items = iter(d.items())


# In[59]:


next(iter_items)


# Here we get an iterator over key, value tuples

# We'll examine the usefullness of being able to iterate using `next` instead of a `for` loop, or comprehension, in the next video.
