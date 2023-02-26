#!/usr/bin/env python
# coding: utf-8

# ### Iterating Callables

# We can easily create iterators that are based on callables in general.
# 
# Let's look at an example:

# ##### Example 1

# In this example we are going to create a counter function (using a closure) - it's a pretty simplistic function - `counter()` will return a closure that we can then call to increment an internal counter by `1` every time it is called:

# In[2]:


def counter():
    i = 0
    
    def inc():
        nonlocal i
        i += 1
        return i
    return inc


# This function allows us to create a simple counter, which we can use as follows:

# In[3]:


cnt = counter()


# In[4]:


cnt()


# In[5]:


cnt()


# Technically we can make an iterator to iterate over this counter:

# In[6]:


class CounterIterator:
    def __init__(self, counter_callable):
        self.counter_callable = counter_callable
        
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.counter_callable()


# Do note that this is an **infinite** iterable!

# In[7]:


cnt = counter()
cnt_iter = CounterIterator(cnt)
for _ in range(5):
    print(next(cnt_iter))


# So basically we were able to create an **iterator** from some arbitrary callable.
# 
# But one issue is that we have an **inifinite** iterable.
# 
# One way around this issue, would be to specify a "stop" value when the iterator should decide to end the iteration.
# 
# Let's see how we would do this:

# In[8]:


class CounterIterator:
    def __init__(self, counter_callable, sentinel):
        self.counter_callable = counter_callable
        self.sentinel = sentinel
        
    def __iter__(self):
        return self
    
    def __next__(self):
        result = self.counter_callable()
        if result == self.sentinel:
            raise StopIteration
        else:
            return result


# Now we can essentially provide a value that if returned from the callable will result in a `StopIteration` exception, essentially terminating the iteration:

# In[9]:


cnt = counter()
cnt_iter = CounterIterator(cnt, 5)
for c in cnt_iter:
    print(c)


# Now there is technically an issue here: the cnt_iter is still "alive" - our iterator raised a `StopIteration` exception, but if we call it again, it will happily resume from where it left off!

# In[10]:


next(cnt_iter)


# We really should make sure the iterator has been consumed, so let's fix that:

# In[11]:


class CounterIterator:
    def __init__(self, counter_callable, sentinel):
        self.counter_callable = counter_callable
        self.sentinel = sentinel
        self.is_consumed = False
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.is_consumed:
            raise StopIteration
        else:
            result = self.counter_callable()
            if result == self.sentinel:
                self.is_consumed = True
                raise StopIteration
            else:
                return result


# Now it should behave as a normal iterator that cannot continue iterating once the first `StopIteration` exception has been raised:

# In[12]:


cnt = counter()
cnt_iter = CounterIterator(cnt, 5)
for c in cnt_iter:
    print(c)


# In[13]:


next(cnt_iter)


# As we just saw, we can essentially make an iterator based on any callable, and our `CounterIterator` was actually quite generic, it only needed a callable and a sentinel value to work.
# 
# In fact, that's exactly what the second form of the `iter()` function allows us to do!

# Let's see the help on `iter`:

# In[16]:


help(iter)


# As we can see `iter` has a second form, that takes in a callable and a sentinel value.
# 
# And it will result in exactly what we have been doing, but without having to create the iterator class ourselves!

# In[17]:


cnt = counter()
cnt_iter = iter(cnt, 5)
for c in cnt_iter:
    print(c)


# In[15]:


next(cnt_iter)


# ##### Example 2

# Both of these approaches can be made to work with any callable.
# 
# For example, you may want to iterate through random numbers until a specific random number is generated:

# In[18]:


import random


# In[25]:


random.seed(0)
for i in range(10):
    print(i, random.randint(0, 10))


# As you can see in this example (I set my seed to 0 to have repeatable results), the number `8` is reached at the `5`th iteration.
# 
# (I am just doing this to find an easy sentinel value so we can easily verify that our code is working properly)

# In[28]:


random_iterator = iter(lambda : random.randint(0, 10), 8)


# In[29]:


random.seed(0)

for num in random_iterator:
    print(num)


# Neat!

# ##### Example 3

# Let's try a countdown example like the one we discussed in the lecture.
# 
# We'll use a closure to get our countdown working:

# In[1]:


def countdown(start=10):
    def run():
        nonlocal start
        start -= 1
        return start
    return run


# In[6]:


takeoff = countdown(10)
for _ in range(15):
    print(takeoff())


# So the countdown function works, but we would like to be able to iterate over it and stop the iteration once we reach 0.

# In[7]:


takeoff  = countdown(10)
takeoff_iter = iter(takeoff, -1)


# In[8]:


for val in takeoff_iter:
    print(val)

