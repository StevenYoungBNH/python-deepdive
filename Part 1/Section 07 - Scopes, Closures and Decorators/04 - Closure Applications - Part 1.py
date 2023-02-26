#!/usr/bin/env python
# coding: utf-8

# ### Closure Applications (Part 1)

# In this example we are going to build an averager function that can average multiple values.
# 
# The twist is that we want to simply be able to feed numbers to that function and get a running average over time, not average a list which requires performing the same calculations (sum and count) over and over again.

# In[1]:


class Averager:
    def __init__(self):
        self.numbers = []
    
    def add(self, number):
        self.numbers.append(number)
        total = sum(self.numbers)
        count = len(self.numbers)
        return total / count


# In[2]:


a = Averager()


# In[3]:


a.add(10)


# In[4]:


a.add(20)


# In[5]:


a.add(30)


# We can do this using a closure as follows:

# In[6]:


def averager():
    numbers = []
    def add(number):
        numbers.append(number)
        total = sum(numbers)
        count = len(numbers)
        return total / count
    return add


# In[7]:


a = averager()


# In[8]:


a(10)


# In[9]:


a(20)


# In[10]:


a(30)


# Now, instead of storing a list and reclaculating `total` and `count` every time wer need the new average, we are going to store the running total and count and update each value each time a new value is added to the running average, and then return `total / count`.
# 
# Let's start with a class approach first, where we will use instance variables to store the running total and count and provide an instance method to add a new number and return the current average.

# In[11]:


class Averager:
    def __init__(self):
        self._count = 0
        self._total = 0
    
    def add(self, value):
        self._total += value
        self._count += 1
        return self._total / self._count


# In[12]:


a = Averager()


# In[13]:


a.add(10)


# In[14]:


a.add(20)


# In[15]:


a.add(30)


# Now, let's see how we might use a closure to achieve the same thing.

# In[16]:


def averager():
    total = 0
    count = 0
    
    def add(value):
        nonlocal total, count
        total += value
        count += 1
        return 0 if count == 0 else total / count
    
    return add
        


# In[17]:


a = averager()


# In[18]:


a(10)


# In[19]:


a(20)


# In[20]:


a(30)


# #### Generalizing this example

# We saw that we were essentially able to convert a class to an equivalent functionality using closures. This is actually true in a much more general sense - very often, classes that define a single method (other than initializers) can be implemented using a closure instead.
# 
# Let's look at another example of this.

# Suppose we want something that can keep track of the running elapsed time in seconds.

# In[21]:


from time import perf_counter


# In[22]:


class Timer:
    def __init__(self):
        self._start = perf_counter()
    
    def __call__(self):
        return (perf_counter() - self._start)


# In[23]:


a = Timer()


# Now wait a bit before running the next line of code:

# In[24]:


a()


# Let's start another "timer":

# In[25]:


b = Timer()


# In[26]:


print(a())
print(b())


# Now let's rewrite this using a closure instead:

# In[27]:


def timer():
    start = perf_counter()
    
    def elapsed():
        # we don't even need to make start nonlocal 
        # since we are only reading it
        return perf_counter() - start
    
    return elapsed


# In[28]:


x = timer()


# In[29]:


x()


# In[30]:


y = timer()


# In[31]:


print(x())
print(y())


# In[32]:


print(a())
print(b())
print(x())
print(y())


# In[ ]:




