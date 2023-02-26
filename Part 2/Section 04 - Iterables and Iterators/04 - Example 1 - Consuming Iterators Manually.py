#!/usr/bin/env python
# coding: utf-8

# ### Consuming Iterators Manually

# We've already seen how to do this:
#
# * get an iterator from the iterable
# * call next on the iterator (until the `StopIteration` exception is raised)

# Let's quickly see how do this again, using a string as the underlying iterable:

# In[1]:
import os

s = 'I sleep all night, and I work all day'


# In[2]:


iter_s = iter(s)


# In[3]:


print(next(iter_s))
print(next(iter_s))
print(next(iter_s))
print(next(iter_s))
print(next(iter_s))


# This means we can get the next item in a collection without actually using a loop of any kind.
#
# Why might this be useful?

# #### Example 1

# A fairly typical use case for this would be when reading data from a CSV file where you know the first few lines consist of information abotu teh data rather than just the data itself.
#
# Let's try this using a CSV file I have saved alongside the Jupyter notebook.

# Let's first load the data and see what it looks like:

# In[4]:

print(os.curdir)
with open('cars.csv') as file:
    for line in file:
        print(line)


# As we can see, the values are delimited by `;` and the first two lines consist of the column names, and column types.
#
# The reason for the spacing between each line is that each line ends with a newline, and our print statement also emits a newline by default. So we'll have to strip those out.

# Here's what we want to do:
# * read the first line to get the column headers and create a named tuple class
# * read data types from second line and store this so we can cast the strings we are reading to the correct data type
# * read the data rows and parse them into a named tuples

# We could do it this way:

# In[5]:


with open('cars.csv') as file:
    row_index = 0
    for line in file:
        if row_index == 0:
            # header row
            headers = line.strip('\n').split(';')
            print(headers)
        elif row_index == 1:
            # data type row
            data_types = line.strip('\n').split(';')
            print(data_types)
        else:
            # data rows
            data = line.strip('\n').split(';')
            print(data)
        row_index += 1


# In[6]:


from collections import namedtuple
cars = []

with open('cars.csv') as file:
    row_index = 0
    for line in file:
        if row_index == 0:
            # header row
            headers = line.strip('\n').split(';')
            Car = namedtuple('Car', headers)
        elif row_index == 1:
            # data type row
            data_types = line.strip('\n').split(';')
            print(data_types)
        else:
            # data rows
            data = line.strip('\n').split(';')
            car = Car(*data)
            cars.append(car)
        row_index += 1


# In[7]:


print(cars[0])


# We still need to parse the data into strings, integers, floats...

# Let's break this problem down into smaller chunks:

# First we need to figure cast to a data type based on the data type string:
# * STRING --> `str`
# * DOUBLE --> `float`
# * INT --> `int`
# * CAT --> `str`

# In[8]:


def cast(data_type, value):
    if data_type == 'DOUBLE':
        return float(value)
    elif data_type == 'INT':
        return int(value)
    else:
        return str(value)


# Next we somehow have to cast all the items in a list, based on their corresponding data type in the data_types array:

# In[9]:


data_types = ['STRING', 'DOUBLE', 'INT', 'DOUBLE',
              'DOUBLE', 'DOUBLE', 'DOUBLE', 'INT', 'CAT']


# In[10]:


data_row = ['Chevrolet Chevelle Malibu', '18.0', '8',
            '307.0', '130.0', '3504.', '12.0', '70', 'US']


# For something like this, we can just zip up the two lists:

# In[11]:


print(list(zip(data_types, data_row)))

# And we can either use a `map()` or a list comprehension to apply the cast function to each one:

# In[12]:


[cast(data_type, value) for data_type, value in zip(data_types, data_row)]


# So now we can write this in a function:

# In[13]:


def cast_row(data_types, data_row):
    return [cast(data_type, value)
            for data_type, value in zip(data_types, data_row)]


# Let's go back and fix up our original code now:

# In[14]:


from collections import namedtuple
cars = []

with open('cars.csv') as file:
    row_index = 0
    for line in file:
        if row_index == 0:
            # header row
            headers = line.strip('\n').split(';')
            Car = namedtuple('Car', headers)
        elif row_index == 1:
            # data type row
            data_types = line.strip('\n').split(';')
        else:
            # data rows
            data = line.strip('\n').split(';')
            data = cast_row(data_types, data)
            car = Car(*data)
            cars.append(car)
        row_index += 1


# In[15]:


cars[0]


# Now let's see if we can clean up this code by using iterators directly:

# In[16]:


from collections import namedtuple
cars = []

with open('cars.csv') as file:
    file_iter = iter(file)
    headers = next(file_iter).strip('\n').split(';')
    Car = namedtuple('Car', headers)
    data_types = next(file_iter).strip('\n').split(';')
    for line in file_iter:
        data = line.strip('\n').split(';')
        data = cast_row(data_types, data)
        car = Car(*data)
        cars.append(car)


# In[17]:


cars[0]


# That's already quite a bit cleaner... But why stop there!

# In[18]:


from collections import namedtuple

with open('cars.csv') as file:
    file_iter = iter(file)
    headers = next(file_iter).strip('\n').split(';')
    data_types = next(file_iter).strip('\n').split(';')
    cars_data = [cast_row(data_types,
                          line.strip('\n').split(';'))
                 for line in file_iter]
    cars = [Car(*item) for item in cars_data]


# In[19]:


print(cars_data[0])


# In[20]:


print(cars[0])


# I chose to split creating the parsed cars_data and the named tuple list into two steps for readability - but we could combine them into a single step:

# In[21]:


from collections import namedtuple

with open('cars.csv') as file:
    file_iter = iter(file)
    headers = next(file_iter).strip('\n').split(';')
    data_types = next(file_iter).strip('\n').split(';')
    cars = [Car(*cast_row(data_types,
                          line.strip('\n').split(';')))
            for line in file_iter]


# In[22]:


print(cars[0])

