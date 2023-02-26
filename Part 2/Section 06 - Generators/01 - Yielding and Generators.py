#!/usr/bin/env python
# coding: utf-8

# ### Yielding and Generators

# Let's start by writing a "simple" iterator first using the techniques we learned in the previous section.

# In[1]:


import math


# In[2]:


class FactIter:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            result = math.factorial(self.i)
            self.i += 1
            return result


# In[3]:


fact_iter = FactIter(5)


# In[4]:


for num in fact_iter:
    print(num)


# We could achieve the same thing using the `iter` method's second form - we just have to know our sentinel value - in this case it would be the factorial of n+1 where n is the last integer's factorial we want our iterator to produce:

# In[5]:


def fact():
    i = 0
    def inner():
        nonlocal i
        result = math.factorial(i)
        i += 1
        return result
    return inner           


# In[6]:


fact_iter = iter(fact(), math.factorial(5))


# In[7]:


for num in fact_iter:
    print(num)


# You'll note that in both cases `fact_iter` was an **iterator**. In the first example we implemented the iterator ourselves, in the second example Python built-it for us.
# 
# The second example was a little less code, but maybe a little more difficult to understand if we were just shown the code without having written it ourselves.
# 
# There has to be a better way!!

# And indeed, there is... generators.

# Let's look at the `yield` statement first.
# 
# The `yield` statement is used almost like a `return` statement in a function - but there is a huge difference - when the `yield` statement is encountered, Python returns whatever value `yield` specifies, but it "pauses" execution of the function. We can then "call" the same function again and it will "resume" from where the last `yield` was encountered.
# 
# I say "call" because we do not "resume" the function by calling it - instead we use the function... `next()` !!!
# 
# Let's try it:

# In[8]:


def my_func():
    print('line 1')
    yield 'Flying'
    print('line 2')
    yield 'Circus'    


# In[9]:


my_func()


# So, executing `my_func()`, returned a generator object - it did not actually "run" the body of `my_func` (none of our print statements actually ran).
# 
# To do that, we need to use the `next()` function. 
# 
# `next()`?? Isn't that what we use for iteration??

# In[10]:


gen_my_func = my_func()


# In[11]:


next(gen_my_func)


# In[12]:


next(gen_my_func)


# And let's call it one more time:

# In[13]:


next(gen_my_func)


# A `StopIteration` exception.
# 
# Hmmm... `next`, `StopIteration`? What does this look like? 
# 
# An **iterator**!

# And in fact that's exactly what Python generators are - they **are** iterators. 

# If generators are iterators, they should implement the iterator **protocol**.
# 
# Let's see:

# In[14]:


gen_my_func = my_func()


# In[15]:


'__iter__' in dir(gen_my_func)


# In[16]:


'__next__' in dir(gen_my_func)


# And so we just have an iterator, which we can use with the `iter()` function and the `next()` function like any other iterator:

# In[17]:


gen_my_func


# In[18]:


iter(gen_my_func)


# As you can see, the `iter` function returned the same object - something we expect with iterators.

# So if this is an iterator that Python builds, how does it know when to stop the iteration (raise the `StopIteration` exception)?
# 
# In the example above, it seemed clear - when the function finished running - there were no more statements after that last `yield`.
# 
# What actually happens if a function finishes running and we don't explicitly return something?
# 
# Remember that Python fills in the gap, and returns `None`.
# 
# In general, the iteration will terminate when we **return** something from the function.
# 
# Let's take a look:

# In[19]:


def squares(sentinel):
    i = 0
    while True:
        if i < sentinel:
            result = i**2
            i += 1
            yield result
        else:
            return 'all done!'


# In[20]:


sq = squares(3)


# In[21]:


next(sq)


# In[22]:


next(sq)


# In[23]:


next(sq)


# In[24]:


next(sq)


# And the return value of our function became the message of the `StopIteration` exception.

# But, we can simplify this slightly:

# In[25]:


def squares(sentinel):
    i = 0
    while True:
        if i < sentinel:
            yield i**2
            i += 1 # note how we can incremenet **after** the yield
        else:
            return 'all done!'


# In[26]:


for num in squares(5):
    print(num)


# So now let's see how we could re-write our initial `factorial` example:

# In[27]:


def factorials(n):
    for i in range(n):
        yield math.factorial(i)    


# In[28]:


for num in factorials(5):
    print(num)


# Now that's a much simpler and understandable way to create the iterator!

# Note that a generator **is** an iterator, but not vice-versa - iterators are not necessarily generators, just like sequences are iterables, but iterables are not necessarily sequences.

# Another thing to note is that since generators are iterators, they also  become exhausted (consumed) just like an iterator does.

# In[29]:


facts = factorials(5)


# In[30]:


list(facts)


# In[31]:


list(facts)


# As you can see, our second iteration through the same generator ended up with nothing - that's because the generator has been exhausted:

# In[32]:


next(facts)

