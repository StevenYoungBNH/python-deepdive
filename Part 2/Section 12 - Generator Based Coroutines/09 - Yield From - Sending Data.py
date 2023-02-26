#!/usr/bin/env python
# coding: utf-8

# ### Yield From - Sending Data

# We have seen how we can send data to a generator by using the generator's `send` method.
# 
# When we use `yield from` to delegate to a subgenerator, the established communication conduit also carries any data sent to the delegator generator.

# Let's write a simple coroutine that will receive string data and print the reversed string to the console:

# In[1]:


def echo():
    while True:
        received = yield
        print(received[::-1])


# We can use this coroutine this way:

# In[2]:


e = echo()
next(e)  # prime the coroutine


# In[3]:


e.send('stressed')


# In[5]:


e.send('tons')


# And we can close the generator:

# In[6]:


e.close()


# Now let's write a simple delegator generator:

# In[17]:


def delegator():
    e = echo()
    yield from e


# We can create the delegator generator and prime the delegator:

# In[18]:


d = delegator()
next(d)


# Now, calling `next` on the delegator will establish the connection to the subgenerator and automatically prime it as well.
# 
# We can easily see this by doing some inspection:

# In[19]:


from inspect import getgeneratorstate, getgeneratorlocals


# In[20]:


getgeneratorlocals(d)


# In[21]:


e = getgeneratorlocals(d)['e']


# In[22]:


print(getgeneratorstate(d))
print(getgeneratorstate(e))


# We can now send data to the delegator, and it will pass that along to the subgenerator:

# In[23]:


d.send('stressed')


# Let's modify our `echo` coroutine to both receive and yield a result, instead of just printing to the console:

# In[25]:


def echo():
    output = None
    while True:
        received = yield output
        output = received[::-1]


# We can use it directly this way:

# In[26]:


e = echo()
next(e)


# In[27]:


e.send('stressed')


# And we can use delegation as follows:

# In[28]:


def delegator():
    yield from echo()


# In[29]:


d = delegator()
next(d)


# In[30]:


d.send('stressed')


# #### Example

# Let's take a look at a more interesting example of `yield from`.
# 
# Our goal is to flatten a list containing nested lists to any level.

# In[1]:


l = [1, 2, [3, 4, [5, 6]], [7, [8, 9, 10]]]


# How could we approach this?
# 
# Let's try a more traditional approach using a recursive function that will build up the flattened list as we work our way through the original nested list.
# 
# Let's start simple, by just printing out the elements as we iterate:

# In[32]:


def flatten(curr_item):
    if isinstance(curr_item, list):
        for item in curr_item:
            flatten(item)
    else:
        print(curr_item)


# In[33]:


flatten(l)


# Now let's create a flattened list instead of just printing the results:

# In[36]:


def flatten(curr_item, output):
    if isinstance(curr_item, list):
        for item in curr_item:
            flatten(item, output)
    else:
        output.append(curr_item)


# In[37]:


output = []
flatten(l, output)
print(output)


# This isn't too bad to understand, but let's try it using generators and `yield from`:

# In[65]:


def flatten_gen(curr_item):
    if isinstance(curr_item, list):
        for item in curr_item:
            yield from flatten_gen(item)
    else:
        yield curr_item        


# In[66]:


for item in flatten_gen(l):
    print(item)


# And of course we can, if we prefer, make a list out of it:

# In[67]:


list(flatten_gen(l))


# I much prefer this approach - first of all we can iterate through the flattened list without making a list out of it - so much better memory wise, and secondly we don't need to lug around that `output` list at every iteration.
# 
# Notice by the way, how we nested subgenerators recursively.

# Technically we can expand this to cover any iterable types - not just lists:

# Let's first create a utility function to see if something is iterable:

# In[68]:


def is_iterable(item):
    try:
        iter(item)
    except:
        return False
    else:
        return True


# In[69]:


def flatten_gen(curr_item):
    if is_iterable(curr_item):
        for item in curr_item:
            yield from flatten_gen(item)
    else:
        yield curr_item


# In[70]:


l = [1, 2, (3, 4, {5, 6}), (7, 8, [9, 10])]


# In[71]:


list(flatten_gen(l))


# But there's potentially a slight wrinkle - strings:

# In[72]:


l = ['abc', [1, 2, (3, 4)]]


# In[73]:


list(flatten_gen(l))


# Why are we getting this recursion error?
# 
# That's because strings are iterables too - even a single character string!
# 
# So, two issues: we may not want to treat strings as iterables, and if we do, then we need to be careful with single character strings.
# 
# We're going to tweak our `is_iterable` function, and our `flatten` generator to handle these two issues:

# In[112]:


def is_iterable(item, *, str_is_iterable=True):
    try:
        iter(item)
    except:
        return False
    else:
        if isinstance(item, str):
            if str_is_iterable and len(item) > 1:
                return True
            else:
                return False
        else:
            return True


# Let's just make sure our function works as expected:

# In[113]:


print(is_iterable([1, 2, 3]))
print(is_iterable('abc'))
print(is_iterable('a'))


# In[114]:


print(is_iterable([1, 2, 3], str_is_iterable=False))
print(is_iterable('abc', str_is_iterable=False))
print(is_iterable('a', str_is_iterable=False))


# Good, now we can tweak our `flatten` generator so we can tell it whether to handle strings as iterables or not:

# In[120]:


def flatten_gen(curr_item, *, str_is_iterable=True):
    if is_iterable(curr_item, str_is_iterable=str_is_iterable):
        for item in curr_item:
            yield from flatten_gen(item, str_is_iterable=str_is_iterable)
    else:
        yield curr_item


# In[121]:


l


# In[122]:


list(flatten_gen(l))


# In[123]:


list(flatten_gen(l, str_is_iterable=False))


# Here we saw we could use `yield from` recursively.
# In fact a generator can be both a delegator and a subgenerator.
# Here's a simple example of this:

# In[6]:


def coro():
    while True:
        received = yield
        print(received)


# In[7]:


def gen1():
    yield from gen2()
    
def gen2():
    yield from gen3()
    
def gen3():
    yield from coro()
    


# In[8]:


g = gen1()
next(g)


# In[9]:


g.send('hello')


# As you can see we were able to push data through a "pipeline":
# 
# ```caller --> gen1 --> gen2 --> gen3 --> coro```

# In[ ]:




