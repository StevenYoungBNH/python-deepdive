#!/usr/bin/env python
# coding: utf-8

# ### Not Just a Context Manager

# Just because our class implements the context manager protocol does not mean it cannot do other things as well!

# In fact the `open` function we use to open files can be used with or without a context manager:

# In[3]:


f = open('test.txt', 'w')
f.writelines('this is a test')
f.close()


# Here we did not use a context manager - the `open` function simply returned the file object - but we had to close the file ourselves - there was not context used.
# 
# On the other hand we can also use it with a context manager:

# In[4]:


with open('test.txt') as f:
    print(f.readlines())


# We can implement classes that implement their own functionality as well as a context manager if we want to.

# ##### Example

# In[2]:


class DataIterator:
    def __init__(self, fname):
        self._fname = fname
        self._f = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        row = next(self._f)
        return row.strip('\n').split(',')
    
    def __enter__(self):
        self._f = open(self._fname)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if not self._f.closed:
            self._f.close()
        return False


# In[3]:


with DataIterator('nyc_parking_tickets_extract.csv') as data:
    for row in data:
        print(row)


# Of course, we cannot use this iterator without also using the context manager since the file would not be opened otherwise:

# In[4]:


data = DataIterator('nyc_parking_tickets_extract.csv')


# In[6]:


for row in data:
    print(row)


# But I want to point out that creating the context manager and using the `with` statement can be done in two steps if we want to:

# In[8]:


data_iter = DataIterator('nyc_parking_tickets_extract.csv')


# At this stage, the object has been created, but the `__enter__` method has not been called yet.
# 
# Once we use `with`, then the file will be opened, and the iterator will be ready for use:

# In[10]:


with data_iter as data:
    for row in data:
        print(row)


# In[ ]:




