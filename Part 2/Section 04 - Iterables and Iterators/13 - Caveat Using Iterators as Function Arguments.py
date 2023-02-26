#!/usr/bin/env python
# coding: utf-8

# ### Caveat of Using Iterators as Function Arguments

# When a function requires an iterable for one of its arguments, it will also work with any iterator (since iterators are themselves iterables).
# 
# But things can go wrong if you do that!

# Let's say we have an iterator that returns a collection of random numbers, and we want, for each such collection, find the minimum amd maximum value:

# In[1]:


import random


# In[2]:


class Randoms:
    def __init__(self, n):
        self.n = n
        self.i = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        else:
            self.i += 1
            return random.randint(0, 100)


# In[3]:


random.seed(0)
l = list(Randoms(10))
print(l)


# Now we can easily find the min and max values:

# In[4]:


min(l), max(l)


# But watch what happens if we do this:

# In[5]:


random.seed(0)
l = Randoms(10)


# In[6]:


min(l)


# In[7]:


max(l)


# That's because when `min` ran, it iterated over the **iterator** `Randoms(10)`. When we called `max` on the same iterator, it had already been exhausted - i.e. the argument to max was now empty!

# So, be really careful when using iterators!

# Here's another more practical example.
# 
# Let's go back to our `cars.csv` data file and write some code that will return the car names and MPG - except we also want to return a value indicating the percentage of the car's MPG to the least fuel efficient car in the list.
# 
# To do so we will need to iterate over the file twice - once to figure out the largest MPG value, and another time to make the calculation MPG/min_mpg * 100.

# Let's just quickly see what our file looks like:

# In[8]:


f = open('cars.csv')
for row in f:
    print(row, end='')
f.close()    


# In[9]:


def parse_data_row(row):
    row = row.strip('\n').split(';')
    return row[0], float(row[1])

def max_mpg(data):
    # get an iterator for data (which should be an iterable of some kind)
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg
    return max_mpg


# In[10]:


f = open('cars.csv')
next(f)
next(f)
print(max_mpg(f))
f.close()


# In[11]:


def list_data(data, mpg_max):
    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / mpg_max * 100
        print(f'{car}: {mpg_perc:.2f}%')


# In[12]:


f = open('cars.csv')
next(f), next(f)
list_data(f, 46.6)
f.close()


# Now let's try and put these together:

# In[13]:


with open('cars.csv') as f:
    next(f)
    next(f)
    max_ = max_mpg(f)
    print(f'max={max_}')
    list_data(f, max_)


# No output from `list_data`!!
# 
# That's because when we called `list_data` we had already exhausted the data file in the call to `max_mpg`.

# Our only option is to either create the iterator twice:

# In[14]:


with open('cars.csv') as f:
    next(f), next(f)
    max_ = max_mpg(f)
    
with open('cars.csv') as f:
    next(f), next(f)
    list_data(f, max_)


# or we could read the entire data set into a list first - but of course if the file is huge we will have some potential for running out memory:

# In[15]:


with open('cars.csv') as f:
    data = [row for row in f][2:]


# or, more simply:

# In[16]:


with open('cars.csv') as f:
    data = f.readlines()[2:]


# In[17]:


max_ = max_mpg(data)
list_data(data, max_)


# We may even write functions that need to iterate more than once over an iterable. For example:

# In[18]:


def list_data(data):
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg
    
    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / max_mpg * 100
        print(f'{car}: {mpg_perc:.2f}%')


# But this will not work if we pass an iterator as the argument:

# with open('cars.csv') as f:
#     next(f)
#     next(f)
#     list_data(f)

# We might want to be more defensive about this in our function, either by raising an exception if the argument is an iterator, or making an iterable from the iterator:

# In[19]:


def list_data(data):
    if iter(data) is data:
        raise ValueError('data cannot be an iterator.')
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg
    
    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / max_mpg * 100
        print(f'{car}: {mpg_perc:.2f}%')


# In[20]:


with open('cars.csv') as f:
    next(f)
    next(f)
    list_data(f)


# or this way:

# In[21]:


def list_data(data):
    if iter(data) is data:
        data = list(data)
    
    max_mpg = 0
    for row in data:
        _, mpg = parse_data_row(row)
        if mpg > max_mpg:
            max_mpg = mpg
    
    for row in data:
        car, mpg = parse_data_row(row)
        mpg_perc = mpg / max_mpg * 100
        print(f'{car}: {mpg_perc:.2f}%')


# In[22]:


with open('cars.csv') as f:
    next(f)
    next(f)
    list_data(f)

