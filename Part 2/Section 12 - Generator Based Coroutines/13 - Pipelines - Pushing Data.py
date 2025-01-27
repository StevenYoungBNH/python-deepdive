#!/usr/bin/env python
# coding: utf-8

# ### Pipelines - Pushing Data

# We can also create pipelines where we **push** data through multiple stages of this pipeline, using `send`, so, essentially, using coroutines.

# First let's create a simple decorator to auto-prime our coroutines:

# In[11]:


def coroutine(coro):
    def inner(*args, **kwargs):
        gen = coro(*args, **kwargs)
        next(gen)
        return gen
    return inner


# Let's start with a data consumer generator that will simply print what it receives - but it could equally well write data to a file, a database, or other processing.

# In[13]:


@coroutine
def handle_data():
    while True:
        received = yield
        print(received)


# Now let's write a coroutine that will receive some data, transform it, and send it along to the next generator:

# In[14]:


import math

@coroutine
def power_up(n, next_gen):
    while True:
        received = yield
        output = math.pow(received, n)
        next_gen.send(output)


# We are going to generate some data, send it to `power_up`, and specify the next stage as being `handle_data`:

# In[15]:


print_data = handle_data()
gen = power_up(2, print_data)
# pipeline: gen --> print_data
for i in range(1, 6):
    gen.send(i)


# Ok, as you can see we are now **pushing** data through this pipeline.
# 
# But why stop there? Let's add another `power_up` in the pipeline:

# In[16]:


print_data = handle_data()
gen2 = power_up(3, print_data)
gen1 = power_up(2, gen2)
# pipeline: gen1 --> gen2 --> print_data
for i in range(1, 6):
    gen1.send(i)


# Now let's add a filter to our pipeline that will only retain even values:

# In[17]:


@coroutine
def filter_even(next_gen):
    while True:
        received = yield
        if received %2 == 0:
            next_gen.send(received)


# And let's insert it as the final stage of our pipeline:

# In[18]:


print_data = handle_data()
filtered = filter_even(print_data)
gen2 = power_up(3, filtered)
gen1 = power_up(2, gen2)

# pipeline: gen1 --> gen2 --> filtered --> print_data

for i in range(1, 6):
    gen1.send(i)


# So as you can see we can easily push data through our pipeline as well.
