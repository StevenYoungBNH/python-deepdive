#!/usr/bin/env python
# coding: utf-8

# ### Yield From - Throwing Exceptions

# We have seen that `yield from` allows us to establish a 2-way communication channel with a subgenerator and we could use `next`, and `send` to send a "request" to a delegated subgenerator via the delegator generator.
# 
# In fact, we can also send exceptions by throwing an exception into the delegator, just like a `send`.

# In[1]:


class CloseCoroutine(Exception):
    pass

def echo():
    try:
        while True:
            received = yield
            print(received)
    except CloseCoroutine:
        return 'coro was closed'
    except GeneratorExit:
        print('closed method was called')


# In[2]:


e = echo()
next(e)


# In[3]:


e.throw(CloseCoroutine, 'just closing')


# In[4]:


e = echo()
next(e)
e.close()


# As we can see the difference between `throw` and `close` is that although `close` causes an exception to be raised in the generator, Python essentially silences it.
# 
# It works the same way when we delegate to the coroutine in a delegator:

# In[5]:


def delegator():
    result = yield from echo()
    yield 'subgen closed and returned:', result
    print('delegator closing...')


# In[6]:


d = delegator()
next(d)
d.send('hello')


# In[7]:


d.throw(CloseCoroutine)


# Now what happens if the `throw` in the subgenerator does not close subgenerator but instead silences the exception and yields a value instead?

# In[8]:


class CloseCoroutine(Exception):
    pass

class IgnoreMe(Exception):
    pass

def echo():
    try:
        while True:
            try:
                received = yield
                print(received)
            except IgnoreMe:
                yield "I'm ignoring you..."
    except CloseCoroutine:
        return 'coro was closed'
    except GeneratorExit:
        print('closed method was called')


# In[9]:


d = delegator()
next(d)


# In[10]:


d.send('python')


# In[11]:


result = d.throw(IgnoreMe, 1000)


# In[12]:


result


# In[13]:


d.send('rocks!')


# Why did we not get a yielded value back?
# 
# That's because the subgenerator was paused at the yield that yielded "I'm, ignoring you".
# 
# If we want to coroutine to continue running normally after ignoring that exception we need to tweak it slightly:

# Let's first make sure we close our previous delegator!

# In[14]:


d.close()


# In[15]:


def echo():
    try:
        output = None
        while True:
            try:
                received = yield output
                print(received)
            except IgnoreMe:
                output = "I'm ignoring you..."
            else:
                output = None
    except CloseCoroutine:
        return 'coro was closed'
    except GeneratorExit:
        print('closed method was called')


# In[16]:


d = delegator()
next(d)


# In[17]:


d.send('hello')


# In[18]:


d.throw(IgnoreMe)


# In[19]:


d.send('python')


# In[20]:


d.close()


# What happens if we do not handle the error in the subgenerator and simply let the exception propagate up?
# Who gets the exception, the delegator, or the caller?

# In[37]:


def echo():
    while True:
        received = yield
        print(received)


# In[38]:


def delegator():
    yield from echo()


# In[39]:


d = delegator()
next(d)


# In[24]:


d.throw(ValueError)


# OK, so we, the caller see the exception. But did the delegator see it too? i.e. can we catch the exception in the delegator?

# In[25]:


def delegator():
    try:
        yield from echo()
    except ValueError:
        print('got the value error')


# In[26]:


d = delegator()
next(d)


# In[27]:


d.throw(ValueError)


# As you can see, we were able to catch the exception in the delegator.
# Of course, the way we wrote our code, the delegator still closed, and hence we now see a `StopIteration` exception.

# #### Example

# Suppose we have a coroutine that creates running averages, and we want to occasionally write the current data to a file:

# In[28]:


class WriteAverage(Exception):
    pass

def averager(out_file):
    total = 0
    count = 0
    average = None
    with open(out_file, 'w') as f:
        f.write('count,average\n')
        while True:
            try:
                received = yield average
                total += received
                count += 1
                average = total / count
            except WriteAverage:
                if average is not None:
                    print('saving average to file:', average)
                    f.write(f'{count},{average}\n')


# In[29]:


avg = averager('sample.csv')
next(avg)


# In[30]:


avg.send(1)
avg.send(2)


# In[31]:


avg.throw(WriteAverage)


# In[32]:


avg.send(3)


# In[33]:


avg.send(2)


# In[34]:


avg.throw(WriteAverage)


# In[35]:


avg.close()


# Now we can read the data back and make sure it worked as expected:

# In[36]:


with open('sample.csv') as f:
    for row in f:
        print(row.strip())


# Of course we can use a delegator as well.
# Maybe the delegator is charged with figuring out the output file name.
# Here we'll just hardcode it inside the delegator:

# In[40]:


def delegator():
    yield from averager('sample.csv')


# In[41]:


d = delegator()
next(d)


# In[42]:


d.send(1)


# In[43]:


d.send(2)


# In[44]:


d.send(3)


# In[45]:


d.send(4)


# In[46]:


d.throw(WriteAverage)


# In[47]:


d.send(5)


# In[48]:


d.throw(WriteAverage)


# In[49]:


d.close()


# In[50]:


with open('sample.csv') as f:
    for row in f:
        print(row.strip())

