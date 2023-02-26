#!/usr/bin/env python
# coding: utf-8

# ### Closure Applications (Part 2)

# #### Example 1

# Let's write a small function that can increment a counter for us - we don't have an incrementor in Python (the ++ operator in Java or C++ for example):

# In[2]:


def counter(initial_value):
    # initial_value is a local variable here
    
    def inc(increment=1):
        nonlocal initial_value
        # initial_value is a nonlocal (captured) variable here
        initial_value += increment
        return initial_value
    
    return inc


# In[3]:


counter1 = counter(0)


# In[4]:


print(counter1(0))


# In[5]:


print(counter1())


# In[6]:


print(counter1())


# In[7]:


print(counter1(8))


# In[8]:


counter2 = counter(1000)


# In[9]:


print(counter2(0))


# In[10]:


print(counter2(1))


# In[11]:


print(counter2())


# In[12]:


print(counter2(220))


# As you can see, each closure maintains a reference to the **initial_value** variable that was created when the **counter** function was **called** - each time that function was called, a new local variable **initial_value** was created (with a value assigned from the argument), and it became a nonlocal (captured) variable in the inner scope.

# #### Example 2

# Let's modify this example to now build something that can run, and maintain a count of how many times we have run some function.

# In[13]:


def counter(fn):
    cnt = 0  # initially fn has been run zero times
    
    def inner(*args, **kwargs):
        nonlocal cnt
        cnt = cnt + 1
        print('{0} has been called {1} times'.format(fn.__name__, cnt))
        return fn(*args, **kwargs)
    
    return inner


# In[14]:


def add(a, b):
    return a + b


# In[15]:


counted_add = counter(add)


# And the free variables are:

# In[16]:


counted_add.__code__.co_freevars


# We can now call the `counted_add` function:

# In[17]:


counted_add(1, 2)


# In[18]:


counted_add(2, 3)


# In[19]:


def mult(a, b, c):
    return a * b * c


# In[20]:


counted_mult = counter(mult)


# In[21]:


counted_mult(1, 2, 3)


# In[22]:


counted_mult(2, 3, 4)


# #### Example 3

# Let's take this one step further, and actually store the function name and the number of calls in a global dictionary instead of just printing it out all the time.

# In[35]:


counters = dict()

def counter(fn):
    cnt = 0  # initially fn has been run zero times
    
    def inner(*args, **kwargs):
        nonlocal cnt
        cnt = cnt + 1
        counters[fn.__name__] = cnt  # counters is global
        return fn(*args, **kwargs)
    
    return inner


# In[26]:


counted_add = counter(add)
counted_mult = counter(mult)


# Note that `counters` is a **global** variable, and therefore **not** a free variable:

# In[27]:


counted_add.__code__.co_freevars


# In[28]:


counted_mult.__code__.co_freevars


# We can now call out functions:

# In[29]:


counted_add(1, 2)


# In[30]:


counted_add(2, 3)


# In[31]:


counted_mult(1, 2, 'a')


# In[32]:


counted_mult(2, 3, 'b')


# In[33]:


counted_mult(1, 1, 'abc')


# In[34]:


print(counters)


# Of course this relies on us creating the **counters** global variable first and making sure we are naming it that way, so instead, we're going to pass it as an argument to the **counter** function:

# In[36]:


def counter(fn, counters):
    cnt = 0  # initially fn has been run zero times
    
    def inner(*args, **kwargs):
        nonlocal cnt
        cnt = cnt + 1
        counters[fn.__name__] = cnt  # counters is nonlocal
        return fn(*args, **kwargs)
    
    return inner


# In[33]:


func_counters = dict()
counted_add = counter(add, func_counters)
counted_mult = counter(mult, func_counters)


# In[34]:


counted_add.__code__.co_freevars


# As you can see, `counters` is now a free variable.

# We can now call our functions:

# In[35]:


for i in range(5):
    counted_add(i, i)

for i in range(10):
    counted_mult(i, i, i)


# In[36]:


print(func_counters)


# Of course, we don't have to assign the "counted" version of our functions a new name - we can simply assign it to the same name!

# In[37]:


def fact(n):
    product = 1
    for i in range(2, n+1):
        product *= i
    return product


# In[38]:


fact = counter(fact, func_counters)


# In[39]:


fact(0)


# In[40]:


fact(3)


# In[41]:


fact(4)


# In[42]:


print(func_counters)


# Notice, how we essentially **added** some functionality to our `fact` function, without modifying what the `fact` function actually returns.
# 
# This leads us straight into our next topic: decorators!

# In[ ]:




