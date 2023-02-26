#!/usr/bin/env python
# coding: utf-8

# ### Closing Generators

# We can actually close a generator by sending it a special message, calling its `close()` method.
# 
# When that happens, an exception is raised **inside** the generator, and we may or may not want to do something - maybe cleaning up a resource, commiting a transaction to a database, etc.

# Let's try it out, without any exception handling first:

# In[1]:


from inspect import getgeneratorstate


# In[2]:


import csv

def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            yield row
    finally:
        print('closing file...')
        f.close()        


# You may notice by the way, that this could easily be turned into a context manager by yielding `reader` instead of yielding individual `rows` from within a loop (as it stands, you cannot make it into a context manager - remember that for context managers there should be a **single** yield!

# In[3]:


import itertools

parser = parse_file('cars.csv')
for row in itertools.islice(parser, 10):
    print(row)


# At this point, we have read 10 rows from the file, but since we have not exhausted our generator, the file is still open.
# 
# How do we close it without iterating through the entire generator?
# 
# Easy, we call the `close()` method on it:

# In[4]:


parser.close()


# And the state of the generator is now closed:

# In[5]:


from inspect import getgeneratorstate


# In[6]:


getgeneratorstate(parser)


# Which means we can no longer call `next()` on it - we'll just get a `StopIteration` exception:

# In[7]:


next(parser)


# What's actually happening is that when we call `close()`, an exception is raised **inside** our generator. Notice that we don't actually catch that exception - we have a finally block, but we do not catch the exception.
# 
# So, an exception is raised while processing that loop, which means our `finally` block runs right away.
# 
# But we are not actually catching the exception, yet we do not actually see the exception appear in our console. This is because that exception is handled specially by Python. When it receives that exception it simply knows that the generator state is now closed.
# 
# This is similar to how the `StopIteration` exception that is raised when we use a `for` loop on an iterator, does not actually show up - Python handles it silently, noting that the iterator is exhausted.

# OK, so now, let's catch that exception inside our generator. The exception is called `GeneratorExit` (and inherits from `BaseException`, not `Exception`, if that matters to you at this point).
# 
# But we have to be careful here - when we call `close()`, Python **expects** one of three things to happen:
# * the generator raises a `GeneratorExit` exception
# * the generator exits cleanly
# * some other exception to be raised - in which case it will propagate the exception to the caller.
# 
# If we trap it, silence it, and try to continue running the generator, Python **will** complain and throw a runtime exception! 
# 
# So, it's OK to catch the exception, but if we do, we need to make sure we re raise it, terminate the function, or raise another exception (but that will bubble up an exception)
# 
# Here's what the Python docs have to say about that:
# 
# ```
# generator.close()
# Raises a GeneratorExit at the point where the generator function was paused. If the generator function then exits gracefully, is already closed, or raises GeneratorExit (by not catching the exception), close returns to its caller. If the generator yields a value, a RuntimeError is raised. If the generator raises any other exception, it is propagated to the caller. close() does nothing if the generator has already exited due to an exception or normal exit.
# ```

# Let's look at an example of this:

# In[8]:


def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            yield row
    except Exception as ex:
        print('some exception occurred', str(ex))
    except GeneratorExit:
        print('Generator was closed!')
    finally:
        print('cleaning up...')
        f.close()        


# Now let's try that again:

# In[9]:


parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)


# In[10]:


parser.close()


# You'll notice that the exception occurred, and then the generator ran the `finally` block and had a clean exit - in other words, the `GeneratorExit` exception was silenced, but the generator terminated (returned), so that's perfectly fine.
# 
# But what happens if we catch that exception inside a loop maybe, and simply ignore it and try to keep going?

# In[11]:


def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('ignoring call to close generator...')
    finally:
        print('cleaning up...')
        f.close()    


# In[12]:


parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)


# In[13]:


parser.close()


# Aha! See, one does not simply ignore the call to `close()` the generator!

# Generators should be cooperative, and ignore a request to close down is not exactly being cooperative.

# If we really want to catch the exception inside our loop, we have to either re-raise it or return from the generator:

# So, both of these will work just fine:

# In[14]:


def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('got a close...')
                raise
    finally:
        print('cleaning up...')
        f.close()    


# In[15]:


parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)


# In[16]:


parser.close()


# As will this:

# In[17]:


def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('got a close...')
                return
    finally:
        print('cleaning up...')
        f.close()   


# In[18]:


parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)


# In[19]:


parser.close()


# And of course, our `finally` block still ran.

# If we want to we can also raise an exception, but this will then be received by the caller, who either has to handle it, or let it bubble up:

# In[20]:


def parse_file(f_name):
    print('opening file...')
    f = open(f_name, 'r')
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        reader = csv.reader(f, dialect=dialect)
        for row in reader:
            try:
                yield row
            except GeneratorExit:
                print('got a close...')
                raise Exception('why, oh why, did you do this?') from None
    finally:
        print('cleaning up...')
        f.close()   


# In[21]:


parser = parse_file('cars.csv')
for row in itertools.islice(parser, 5):
    print(row)


# In[22]:


parser.close()


# Another very important point to note is that the `GeneratorExit` exception does not inherit from `Exception` - because of that, you can still trap an `Exception`, even very broadly, without accidentally catching, and potentially silencing, a `GeneratorExit` exception.
# 
# We'll see an example of this next.

# So, what about applying the same `close()` to generators acting not as iterators, but as coroutines?

# Suppose we have a generator whose job is to open a database transaction, receive data to be written to the database, and then commit the transactions to the database once the work is "over".

# We can certainly do it using a context manager - but we can also do it using a coroutine.

# In[23]:


def save_to_db():
    print('starting new transaction')
    while True:
        try:
            data = yield
            print('sending data to database:', data)
        except GeneratorExit:
            print('committing transaction')
            raise


# In[24]:


trans = save_to_db()


# In[25]:


next(trans)


# In[26]:


trans.send('data 1')


# In[27]:


trans.send('data 2')


# In[28]:


trans.close()


# But of course, something could go wrong while writing the data to the database, in which case we would want to abort the transaction instead:

# In[5]:


def save_to_db():
    print('starting new transaction')
    while True:
        try:
            data = yield
            print('sending data to database:', eval(data))
        except Exception:
            print('aborting transaction')  
        except GeneratorExit:
            print('committing transaction')
            raise


# In[6]:


trans = save_to_db()
next(trans)


# In[7]:


trans.send('1 + 10')


# In[8]:


trans.send('1/0')


# But we have a slight problem:

# In[34]:


trans.send('2 + 2')


# We'll circle back to this in a bit.

# But we can still commit the transaction when things do not go wrong:

# In[35]:


trans = save_to_db()
next(trans)
trans.send('1+10')
trans.send('2+10')
trans.close()


# OK, so this works but is far from ideal:
# 
# 1. We do not know that an exception occurred and that a rollback happened (well we do from the console output, but not programmatically)
# 2. if an abort took place, we really need to close the generator
# 3. It would be safer to have a `finally` clause, that either commits or rollbacks the transaction - we could have an exception that is not caught by any of our exception handlers - and that would be a problem!
# 
# Let's fix those issues up:

# In[36]:


def save_to_db():
    print('starting new transaction')
    is_abort = False
    try:
        while True:
            data = yield
            print('sending data to database:', eval(data))
    except Exception:
        is_abort = True
        raise
    finally:
        if is_abort:
            print('aborting transaction')
        else:
            print('committing transaction')


# Notice how we're not even catching the `GeneratorExit` exception - we really don't need to - that exception will be raised, the `finally` block will run, and the `GeneratorExit` exception will be bubbled up to Python who will expect it after the call to `close()`

# In[37]:


trans = save_to_db()
next(trans)
trans.send('1 + 1')
trans.close()


# In[38]:


trans = save_to_db()
next(trans)
trans.send('1 / 0')

