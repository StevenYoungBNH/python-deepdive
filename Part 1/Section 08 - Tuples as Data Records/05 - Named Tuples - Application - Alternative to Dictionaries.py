#!/usr/bin/env python
# coding: utf-8

# ### Named Tuples - Application - Alternative to Dictionaries

# First an important caveat: all this really only works for dictionaries with **string** keys. Dictionary keys can be other hashable data types, (including tuples, as long as they contain hashable types in turn), and these examples will not work with those types of dictionaries.

# In[4]:


from collections import namedtuple


# In[11]:


data_dict = dict(key1=100, key2=200, key3=300)


# In[12]:


Data = namedtuple('Data', data_dict.keys())


# In[13]:


Data._fields


# Now we can create an instance of the `Data` named tuple using the data in the `data_dict` dictionary. 
# 
# We could try the following (bad idea):

# In[15]:


d1 = Data(*data_dict.values())


# In[16]:


d1


# This looks like it worked. 
# 
# But consider this second dictionary, where we do not create the keys in the same order:

# In[35]:


data_dict_2 = dict(key1=100, key3=300, key2=200)


# In[36]:


d2 = Data(*data_dict_2.values())


# In[37]:


d2


# Obviously this went terribly wrong!
# 
# We cannot guarantee that the order of `values()` will be in the same order as the keys (in our named tuple and in the dictionary).
# 
# Instead, we should unpack the dictionary itself, resulting in keyword arguments that will be passed to the `Data` constructor:

# In[38]:


d2 = Data(**data_dict_2)


# In[39]:


d2


# So, the pattern to create a named tuple out of a single dictionary is straightforward:
# 
# For any dictionary `d` we can created a named tuple class and insert the data into it as follows:
# 
# `1. Struct = namedtuple('Struct', d.keys())`
# 
# `2. data = Struct(**d)`

# Because dictionaries now preserve key order, the order of the fields in the named tuple structure will be the same. If you want your fields to be sorted in a different way, just sort the keys when you create the named tuple class. For example, to have keys sorted alphabetically we could do:

# In[40]:


data_dict = dict(first_name='John', last_name='Cleese', age=42, complaint='dead parrot')


# In[41]:


data_dict.keys()


# In[44]:


sorted(data_dict.keys())


# In[45]:


Struct = namedtuple('Struct', sorted(data_dict.keys()))


# In[46]:


Struct._fields


# Of course we can still put in the correct values from the dictionary into the correct slots in the tuple by unpacking the dictionary instead of just the values:

# In[48]:


d1 = Struct(**data_dict)


# In[49]:


d1


# And of course, since this is now a named tuple we can access the data using the field name:

# In[50]:


d1.complaint


# instead of how we would have done it with the dictionary:

# In[51]:


data_dict['complaint']


# I also want to point out that with dictionaries we often end up with code where the key is stored in some variable and then referenced this way:

# In[53]:


key_name = 'age'
data_dict[key_name]


# We cannot use this approach directly with named tuples however. For example this will not work:

# In[54]:


key_name = 'age'
d1.key_name


# However, we can use the `getattr` function that we have seen before:

# In[57]:


key_name = 'age'
getattr(d1, key_name)


# We also have the `get` method on dictionaries that can specify a default value to return if the key does not exist:

# In[59]:


data_dict.get('age', None), data_dict.get('invalid_key', None)


# And we can do the same with the `getattr` function:

# In[60]:


getattr(d1, 'age', None), getattr(d1, 'invalid_field', None)


# Now this is not very useful if you are only working with a single instance of a dictionary that has the same set of keys. Kind of pointless really.
# 
# You also do not want to create a new named tuple for every instance of a dictionary - that would just be way too much overhead.
# 
# But in cases where you have a collection of dictionaries that share a common set of keys, this can be really useful, as long as you are willing to live with the fact that you now have immutable structures.

# Let's suppose we have this data list:

# In[3]:


data_list = [
    {'key1': 1, 'key2': 2},
    {'key1': 3, 'key2': 4},
    {'key1': 5, 'key2': 6, 'key3': 7},
    {'key2': 100}
]


# The first thing to note is that we need to figure out all the possible keys that have been used in the dictionaries in this list.

# The easiest way to do this is to extract all the keys of all the dictionaries and then make a `set` out of them, to eliminate duplicate key names:

# We could do it this way, using a simple loop:

# In[79]:


keys = set()
for d in data_list:
    for key in d.keys():
        keys.add(key)


# In[80]:


keys


# But actually a more efficient way would be to use a comprehension:

# In[110]:


keys = {key for dict_ in data_list for key in dict_.keys()}


# In[111]:


keys


# In fact, we can also use the fact that we can union multiple sets (we'll cover this in detail later) by unpacking all the keys and creating a union of them:

# In[114]:


keys = set().union(*(dict_.keys() for dict_ in data_list))


# In[115]:


keys


# However you do it, we end up with a set of all the possible keys used in our list of dictionaries.

# Now we can go ahead and create a named tuple with all those keys as fields:

# In[117]:


Struct = namedtuple('Struct', keys)


# In[118]:


Struct._fields


# As you can see, sets do not preserve order, so in this case we'll probably sort the keys to create our named tuple:

# In[119]:


Struct = namedtuple('Struct', sorted(keys))


# In[120]:


Struct._fields


# Now, we're also going to provide default values, since not all dictionaries have all the keys in them. In this case I'm going to set the default to `None` if the key is missing:

# In[121]:


Struct.__new__.__defaults__ = (None,) * len(Struct._fields)


# Now we're ready to load up all these dictionaries into a new list of named tuples:

# In[122]:


tuple_list = [Struct(**dict_) for dict_ in data_list]


# In[123]:


tuple_list


# So lastly, let's just package this all up neatly into a single function that will take an iterable of dictionaries, or an arbitrary number of dictionaries as positional arguments, and return a list of named tuples:

# In[5]:


def tuplify_dicts(dicts):
    keys = {key for dict_ in dicts for key in dict_.keys()}
    Struct = namedtuple('Struct', keys)
    Struct.__new__.__defaults__ = (None,) * len(Struct._fields)
    return [Struct(**dict_) for dict_ in dicts]


# In[6]:


tuplify_dicts(data_list)


# Isn't Python wonderful? :-)
