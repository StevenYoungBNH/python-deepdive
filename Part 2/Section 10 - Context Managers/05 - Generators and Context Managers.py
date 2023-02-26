#!/usr/bin/env python
# coding: utf-8

# ### Generators and Context Managers

# Let's see how we might write something that almost behaves like a context manager, using a generator function:

# In[1]:


def my_gen():
    try:
        print('creating context and yielding object')
        lst = [1, 2, 3, 4, 5]
        yield lst
    finally:
        print('exiting context and cleaning up')


# In[2]:


gen = my_gen()  # create generator


# In[3]:


lst = next(gen)  # enter context and get "as" object


# In[4]:


print(lst)


# In[5]:


next(gen)  # exit context


# As you can see, the exiting context code ran.
# But to make this cleaner, we'll catch the StopIteration exception:

# In[6]:


gen = my_gen()
lst = next(gen)
print(lst)
try:
    next(gen)
except StopIteration:
    pass


# Now let's write a context manager that can use the type of generator we wrote so we can use it using a `with` statement instead:

# In[7]:


class GenCtxManager:
    def __init__(self, gen_func):
        self._gen = gen_func()
        
    def __enter__(self):
        return next(self._gen)
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            next(self._gen)
        except StopIteration:
            pass
        return False


# In[8]:


with GenCtxManager(my_gen) as lst:
    print(lst)


# Our `GenCtxManager` class is not very flexible - we cannot pass arguments to the generator function for example. We are also not doing any exception handling...

# We could try some of this ourselves. 
# For example handling arguments:

# In[9]:


class GenCtxManager:
    def __init__(self, gen_func, *args, **kwargs):
        self._gen = gen_func(*args, **kwargs)
        
    def __enter__(self):
        return next(self._gen)
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            next(self._gen)
        except StopIteration:
            pass
        return False


# In[10]:


def open_file(fname, mode):
    try:
        print('opening file...')
        f = open(fname, mode)
        yield f
    finally:
        print('closing file...')
        f.close()


# In[11]:


with GenCtxManager(open_file, 'test.txt', 'w') as f:
    print('writing to file...')
    f.write('testing...')


# In[12]:


with open('test.txt') as f:
    print(next(f))


# This works, but is not very elegant, and we still are not doing much exception handling. 
# In the next video, we'll look at a decorator in the standard library that does this far more robustly and elegantly...
