#!/usr/bin/env python
# coding: utf-8

# ### Project 6 - Solution

# The first thing I'm going to do is to simply copy the `parse_data` code from the pull pipeline example - we can reuse that code:

# In[1]:


import csv

def parse_data(f_name):
    f = open(f_name)
    try:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)  # skip header row
        yield from csv.reader(f, dialect=dialect)
    finally:
        f.close()


# Since we're going to be creating coroutines, we're going to find a coroutine decorator to auto prime coroutines useful:

# In[2]:


def coroutine(fn):
    def inner(*args, **kwargs):
        coro = fn(*args, **kwargs)
        next(coro)
        return coro
    return inner


# Let's start writing the various coroutines and functions we are going to need for our pipeline:
# 
# * coroutine to save data to a file
# * coroutine to filter data based on the vehicle name - but we'll make it generic and use a filter function (predicate) as an argument
# * coroutine to act as the pipeline
# * a context manager that will open and close the pipeline automatically

# In[7]:


@coroutine
def save_csv(f_name):
    with open(f_name, 'w', newline='') as f:
        writer = csv.writer(f)
        while True:
            row = yield
            writer.writerow(row)


# In[84]:


@coroutine
def filter_data(filter_pred, target):
    while True:
        row = yield
        if filter_pred(row):
            target.send(row)


# Now we need to create our custom pipeline that will create the various coroutines with appropriate filters, as well as the `save_csv` coroutine, and orchestrates the data flow:

# In[89]:


@coroutine
def pipeline_coro(out_file, name_filters):
    save = save_csv(out_file)
    
    target = save
    for name_filter in name_filters:
        target = filter_data(lambda d, v=name_filter: v in d[0], target)
        # warning: we have to use the trick above because
        # lambdas are actually closures and the free variable name_filter
        # is a shared free variable - we have seen this problem before!
    while True:
        received = yield
        target.send(received)


# Next, we are going to create a context manager to automatically close the pipeline when we are done with it:

# In[86]:


from contextlib import contextmanager

@contextmanager
def pipeline(out_file, name_filters):
    p = pipeline_coro(out_file, name_filters)
    try:
        yield p
    finally:
        p.close()


# And now we can start using the pipeline:

# In[87]:


with pipeline('out.csv', ('Chevrolet', 'Landau', 'Carlo')) as p:
    for row in parse_data('cars.csv'):
        p.send(row)


# And finally let's make sure the data was written out correctly:

# In[88]:


with open('out.csv') as f:
    for row in f:
        print(row, end='')


# Perfect!
