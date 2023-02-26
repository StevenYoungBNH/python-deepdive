#!/usr/bin/env python
# coding: utf-8

# ### Sending Exceptions to Generators

# So far we have seen how to send values to a generator using the `send()` method.
# 
# We have also seen how we can close a generator using the `close()` method and how that, in essence, raises a `GeneratorExit` exception inside the generator.
# 
# In fact we can also raise any exception inside a generator by using the `throw()` method.
# 
# Let's first see a simple example:

# In[1]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('exception must have happened...')


# In[2]:


g = gen()


# In[3]:


next(g)


# In[4]:


g.send('hello')


# In[5]:


g.throw(ValueError, 'custom message')


# As you can see, the exception occurred **inside** the generator, and then propagated up to the caller (we did not intercept and silence the exception). Of course we can do that if we want to:

# In[6]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError:
        print('received the value error...')
    finally:
        print('generator exiting and closing')


# In[7]:


g = gen()


# In[8]:


next(g)
g.send('hello')


# In[9]:


g.throw(ValueError, 'stop it!')


# We caught the `ValueError` exception, so why did we get a `StopIteration` exception?
# 
# Because the generator returned - this raises a `StopIteration` exception.

# The behavior of the `throw` is as follows:
# 
# * if the generator catches the exception and yields a value, that is the return value of the `throw()` method
# * if the generator does not catch the exception, the exception is propagated back to the caller
# * if the generator catches the exception, and exits (returns), the `StopIteration` exception is propagated to the caller
# * if the generator catches the exception, and raises another exception, that exception is propagated to the caller

# Let's see an example of each of those:

# ##### if the generator catches the exception and yields a value, that is the return value of the throw() method

# In[11]:


from inspect import getgeneratorstate


# In[12]:


def gen():
    while True:
        try:
            received = yield
            print(received)
        except ValueError as ex:
            print('ValueError received...', ex)


# In[13]:


g = gen()
next(g)


# In[14]:


g.send('hello')


# In[15]:


g.throw(ValueError, 'custom message')


# In[16]:


g.send('hello')


# And the generator is now in a suspended state, waiting for our next call:

# In[17]:


getgeneratorstate(g)


# ##### if the generator does not catch the exception, the exception is propagated back to the caller

# In[18]:


def gen():
    while True:
        received = yield
        print(received)


# In[19]:


g = gen()
next(g)
g.send('hello')


# In[20]:


g.throw(ValueError, 'custom message')


# And the generator is now in a closed state:

# In[21]:


getgeneratorstate(g)


# ##### if the generator catches the exception, and exits (returns), the StopIteration exception is propagated to the caller

# In[22]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError as ex:
        print('ValueError received', ex)
        return None


# In[23]:


g = gen()
next(g)
g.send('hello')


# In[24]:


g.throw(ValueError, 'custom message')


# And, once again, the generator is in a closed state:

# In[25]:


getgeneratorstate(g)


# ##### if the generator catches the exception, and raises another exception, that exception is propagated to the caller

# In[26]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError as ex:
        print('ValueError received...', ex)
        raise ZeroDivisionError('not really...')


# In[27]:


g = gen()
next(g)
g.send('hello')


# In[28]:


g.throw(ValueError, 'custom message')


# And out generator is, once again, in a closed state:

# In[29]:


getgeneratorstate(g)


# As you can see our traceback includes both the `ZeroDivisionError` and the `ValueError` that caused the `ZeroDivisionError` to happen in the first place. If you don't want to have that  traceback you can easily remove it and only display the `ZeroDivisionError` (I will cover this and exceptions in detail in a later part of this series):

# In[30]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    except ValueError as ex:
        print('ValueError received...', ex)
        raise ZeroDivisionError('not really...') from None


# In[31]:


g = gen()
next(g)
g.send('hello')


# In[32]:


g.throw(ValueError, 'custom message')


# #### Example of where this can be useful

# Suppose we have a coroutine that handles writing data to a database.
# We have seen in some previous examples where we could use a coroutine to start and either commit or abort a transaction - based on closing the generator or forcing an exception to happen in the body of the generator.
# 
# Let's revisit this example, but now we'll want to use exceptions to indicate to our generator whether to commit or abort a transaction, without necessarily exiting the generator:

# In[33]:


class CommitException(Exception):
    pass

class RollbackException(Exception):
    pass

def write_to_db():
    print('opening database connection...')
    print('start transaction...')
    try:
        while True:
            try:
                data = yield
                print('writing data to database...', data)
            except CommitException:
                print('committing transaction...')
                print('opening next transaction...')
            except RollbackException:
                print('aborting transaction...')
                print('opening next transaction...')
    finally:
        print('generator closing...')
        print('aborting transaction...')
        print('closing database connection...')


# In[34]:


sql = write_to_db()


# In[35]:


next(sql)


# In[36]:


sql.send(100)


# In[37]:


sql.throw(CommitException)


# In[38]:


sql.send(200)


# In[39]:


sql.throw(RollbackException)


# In[40]:


sql.send(200)
sql.throw(CommitException)
sql.close()


# As you can see, we can use exceptions to control the **flow** of our code. Exceptions are not necessarily **errors**! As we have seen with the `StopIteration` exception, or the `GeneratorExit` exception.

# #### throw() and close()

# The `close()` method does essentially the same thing as `throw(GeneratorExit)` except that when that exception is thrown using `throw()`, Python does not silence the exception for the caller:

# In[41]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    finally:
        print('closing down...')


# In[42]:


g = gen()
next(g)
g.send('hello')
g.close()


# In[45]:


g = gen()
next(g)
g.send('hello')
g.throw(GeneratorExit)


# Even if we catch the exception, we are still exiting the generator, so using `throw` will result in the caller receiving a `StopIteration` exception.

# In[46]:


def gen():
    try:
        while True:
            received = yield
            print(received)
    except GeneratorExit:
        print('received generator exit...')
    finally:
        print('closing down...')


# In[47]:


g = gen()
next(g)
g.close()


# In[48]:


g = gen()
next(g)
g.throw(GeneratorExit)


# So, we can use `throw` to close the generator, but as the caller we now have to handle the exception that propagates up to us:

# In[49]:


g = gen()
next(g)
try:
    g.throw(GeneratorExit)
except StopIteration:
    print('silencing GeneratorExit...')
    pass
        


# Basically this is the exact same scenario as the catch and exit (return) we saw a couple of examples back.
