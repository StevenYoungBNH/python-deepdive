#!/usr/bin/env python
# coding: utf-8

# ### Using Decorators to Create Context Managers using Generator Functions

# In the last video we saw how we could create a generic class that could take a generator function that had a specific structure and turn it into a context manager.
# 
# Let's see if we can do one step better, using a decorator instead.

# Recall the basic structure our generator function needs to have:
# 
# ```
# def gen(args):
#     # set up happens here, or inside try
#     try:
#         yield obj # whatever normally gets returned by __enter__
#     finally:
#         # perform clean up code here
# ```

# First let's define a generator function to open a file, yield it, and then close it - same as the example we saw in the previous video:

# In[1]:


def open_file(fname, mode='r', encoding='UTF-8'):
    print('opening file...')
    f = open(fname, mode, encoding=encoding, buffering=1)
    print(f'f is: {f}')
    try:
        yield f
    finally:
        print('closing file...')
        f.close()


# Next, let's re-create the context manager wrapper we did in the last video, but this time, I'm going to pass it a generator object, instead of a generator function. But basically the same idea:

# In[4]:


class GenContextManager:
    def __init__(self, gen):
        self.gen = gen
        
    def __enter__(self):
        print(f'At __enter__')
        return next(self.gen) # need to prime the generator
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        print('calling next to perform cleanup in generator')
        try:
            next(self.gen)
        except StopIteration:
            print('StopIteration received')
            pass
        return False


# At this point we can use this with our generator function as follows:

# In[5]:


file_gen = open_file('test.txt', 'w')

with GenContextManager(file_gen) as f:
    print('Writing output to file...')
    f.writelines('Sir Spamalot\n')
    f.writelines('extra test line 1\n')
    f.writelines('extra test line 2\n')
    print('Exiting out of context manager')


# And we can read back from the file too:

# In[9]:


file_gen = open_file('test.txt', 'rt', encoding='UTF-8')
# file_gen = open('test.txt', 'rt', encoding='UTF-8')

# line = file_gen.readline()
with GenContextManager(file_gen) as f:
    print(f.readline())
    for line in f:
        
        print(line)


# Of course, our context manager object is not very robust - there is no exception handling for example. But let's leave that "minor detail" aside for now :-)

# We still have to create the generator object from the generator function before we can use the context manager class.
# 
# We can simplify things even more by using a decorator:

# In[24]:


def context_manager_dec(gen_fn):
    def helper(*args, **kwargs):
        gen = gen_fn(*args, **kwargs)
        ctx = GenContextManager(gen)
        return ctx
    return helper


# Notice what this decorator does.
# 
# It decorates a generator function and returns `helper`. When we invoke `helper` it will create an instance of the generator, and create and return an instance of the context manager.
# 
# Let's try it out:

# In[25]:


@context_manager_dec
def open_file(fname, mode='r'):
    print('opening file...')
    f = open(fname, mode)
    try:
        yield f
    finally:
        print('closing file...')
        f.close()    


# In[26]:


with open_file('test.txt') as f:
    print(f.readlines())


# So now we have an approach to using a decorator to turn any generator function (that has the structure we mentioned earlier) into a context manager!
# 
# Our code was not very robust, either in the context manager class or in the decorator - and it would take quite a bit more work to make it so.
# 
# Fortunately the standard library already has this implemented for us - in fact that was one of the critical goals of Python's context managers - the ability to create context managers using generator functions (see PEP 343).

# In[27]:


from contextlib import contextmanager


# In[33]:


@contextmanager
def open_file(fname, mode='r'):
    print('opening file...')
    f = open(fname, mode)
    try:
        yield f
    finally:
        print('closing file...')
        f.close() 


# In[34]:


with open_file('test.txt') as f:
    print(f.read())


# And of course, this works for more than just opening and closing files. 
# 
# Here are some more examples:

# #### Example 1

# Let's implement a timer.

# In[35]:


from time import perf_counter, sleep


# In[36]:


@contextmanager
def timer():
    stats = dict()
    start = perf_counter()
    stats['start'] = start
    yield stats
    end = perf_counter()
    stats['end'] = end
    stats['elapsed'] = end - start


# In[37]:


with timer() as stats:
    sleep(1)


# In[38]:


print(stats)


# #### Example 2

# In this example, let's redirect `stdout`.

# In[39]:


import sys


# In[40]:


@contextmanager
def out_to_file(fname):
    current_stdout = sys.stdout
    file = open(fname, 'w')
    sys.stdout = file
    try:
        yield None
    finally:
        file.close()
        sys.stdout = current_stdout


# In[41]:


with out_to_file('test.txt'):
    print('line 1')
    print('line 2')


# In[42]:


with open('test.txt') as f:
    print(f.readlines())


# And of course, `stdout` is back to "normal":

# In[19]:


print('line 1')


# The `contextlib` module actually implements a `stdout` redirect context manager, so we technically don't have to write one ourselves.
# 
# The difference from the one we wrote is that it needs an open file object, not just a file name. So we would have to open the file, then redirect stdout. We can do this easily by nesting two context managers as follows:

# In[20]:


from contextlib import redirect_stdout


# In[21]:


with open('test.txt', 'w') as f:
    with redirect_stdout(f):
        print('Look on the bright side of life')


# And we can check that this worked:

# In[22]:


with open('test.txt') as f:
    print(f.readlines())

