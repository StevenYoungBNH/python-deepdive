#!/usr/bin/env python
# coding: utf-8

# ### Updating, Merging and Copying

# Updating an existing key's value in a dictionary is straightforward:

# In[1]:


d = {'a': 1, 'b': 2, 'c': 3}


# In[2]:


d['b'] = 200


# In[3]:


d


# #### The `update` method

# Sometimes however, we want to update all the items in one dictionary based on items in another dictionary.

# For that we can use the `update` method.

# The `update` method has three forms:
# 1. it can take another dictionary
# 2. it can take an iterable of iterables of length 2 (key, value)
# 3. if can take keyword arguments
# 
# You'll notice that the arguments we can use with `update` is very similar to the type of arguments we can use with the `dict()` function when we create dictionaries.

# Let's look briefly at each of those forms:

# In[4]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}


# In[5]:


d1.update(d2)
print(d1)


# Note how the key order is maintained and based on the order in which the dictionaries were create/updated.

# In[6]:


d1 = {'a': 1, 'b': 2}


# In[7]:


d1.update(b=20, c=30)
print(d1)


# Again notice how the key order reflects the order in which the parameters were specified when calling the `update` method.

# In[8]:


d1 = {'a': 1, 'b': 2}


# In[9]:


d1.update([('c', 2), ('d', 3)])


# In[10]:


d1


# Of course we can use more complex iterables. For example we could use a generator expression:

# In[11]:


d = {'a': 1, 'b': 2}
d.update((k, ord(k)) for k in 'python')
print(d)


# So far we have updated dictionaries with other dictionaries or iterables that do not contain the same keys. Sometimes that does happen - in that case, the corresponding key in the dictionary being updated has it's associated value replaced by the new value:

# In[12]:


d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 200, 'd': 4}
d1.update(d2)
print(d1)


# #### Unpacking dictionaries

# We can also use unpacking to unpack the contents of one dictionary into the elements of another dictionary. This is very similar to how we can unpack iterables. Let's recall that first:

# In[13]:


l1 = [1, 2, 3]
l2 = 'abc'
l = (*l1, *l2)
print(l)


# We can do something similar with dictionaries:

# In[14]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d = {**d1, **d2}
print(d)


# Again note how order is preserved.
# What happens when there are conflicting keys in the unpacking?

# In[15]:


d1 = {'a': 1, 'b': 2}
d2 = {'b': 200, 'c': 3}
d = {**d1, **d2}
print(d)


# As you can see, the 'last' key/value pair wins.
# 
# Now the nice thing about unpacking is that we are not limited to just two dictionaries.

# ##### Example

# In this example we have some dictionaries we use to configure our application.
# One dictionary specifies some configuration defaults for every configuration parameter our application will need.
# Another dictionary is used to configure some global configuration, and another set of dictionaries is used to define environment specific configurations, maybe dev and prod.

# In[16]:


conf_defaults = dict.fromkeys(('host', 'port', 'user', 'pwd', 'database'), None)
print(conf_defaults)


# In[17]:


conf_global = {
    'port': 5432,
    'database': 'deepdive'}


# In[18]:


conf_dev = {
    'host': 'localhost',
    'user': 'test',
    'pwd': 'test'
}

conf_prod = {
    'host': 'prodpg.deepdive.com',
    'user': '$prod_user',
    'pwd': '$prod_pwd',
    'database': 'deepdive_prod'
}


# Now we can generate a full configuration for our dev environment this way:

# In[19]:


config_dev = {**conf_defaults, **conf_global, **conf_dev}


# In[20]:


print(config_dev)


# and a config for our prod environment:

# In[21]:


config_prod = {**conf_defaults, **conf_global, **conf_prod}


# In[22]:


print(config_prod)


# ##### Example

# Another way dictionary unpacking can be really useful, is for passing keyword arguments to a function:

# In[23]:


def my_func(*, kw1, kw2, kw3):
    print(kw1, kw2, kw3)


# In[24]:


d = {'kw2': 20, 'kw3': 30, 'kw1': 10}


# In this case, we don't really care about the order of the elements, since we'll be unpacking keyword arguments:

# In[25]:


my_func(**d)


# Of course we can even use it this way, but here the dictionary order does matter, as it will be reflected in the order in which those arguments are passed to the function:

# In[26]:


def my_func(**kwargs):
    for k, v in kwargs.items():
        print(k, v)


# In[27]:


my_func(**d)


# As you can see the function's `kwargs` dictionary received the elements in the same order as the original dictionary we unpacked.

# #### Copying Dictionaries

# We can make copies of dictionaries. But as with iterables, we have to differentiate between **shallow** and **deep** copies.

# The `copy` method that dictionaries implement is a shallow copy mechanism.
# This means that a new container is created, but the item references within the collection are maintained.
# 
# Let's see a simple example:

# In[28]:


d = {'a': [1, 2], 'b': [3, 4]}


# In[29]:


d1 = d.copy()


# In[30]:


print(d)
print(d1)


# In[31]:


id(d), id(d1), d is d1


# So `d` and `d1` are not the same objects, so we can add and remove keys from one dict without affecting the other. Also, we can completely replace an associated value in one without affecting the other.

# In[32]:


del d['a']


# In[33]:


print(d)
print(d1)

or even:
# In[34]:


d['b'] = 100


# In[35]:


print(d)
print(d1)


# But let's see what happens if we mutate the value of one dictionary:

# In[36]:


d = {'a': [1, 2], 'b': [3, 4]}
d1 = d.copy()
print(d)
print(d1)


# In[37]:


d['a'].append(100)


# In[38]:


print(d)


# In[39]:


print(d1)


# As you can see the mutation was also "seen" by `d1`. This is because the objects `d['a']` and `d1['a']` are in fact the **same** objects.

# In[40]:


d['a'] is d1['a']


# So if we have nested dictionaries for example, as is often the case with JSON documents, we have to be careful when creating shallow copies.

# In[41]:


d = {'id': 123445,
    'person': {
        'name': 'John',
        'age': 78},
     'posts': [100, 105, 200]
    }


# In[42]:


d1 = d.copy()


# In[43]:


d1['person']['name'] = 'John Cleese'
d1['posts'].append(300)


# In[44]:


d1


# In[45]:


d


# If we want to avoid this issue, we have to create a **deep** copy.
# We can easily do this ourselves using recursion, but the `copy` module implements such a function for us:

# In[46]:


from copy import deepcopy


# In[47]:


d = {'id': 123445,
    'person': {
        'name': 'John',
        'age': 78},
     'posts': [100, 105, 200]
    }


# In[48]:


d1 = deepcopy(d)


# In[49]:


d1['person']['name'] = 'John Cleese'
d1['posts'].append(300)


# In[50]:


d1


# In[51]:


d


# We saw earlier that we can also copy a dictionary by essentially unpacking the keys of one, or more dictionaries, into another.
# This also creates a **shallow** copy:

# In[52]:


d1 = {'a': [1, 2], 'b':[3, 4]}
d = {**d1}


# In[53]:


d


# In[54]:


d1['a'].append(100)


# In[55]:


d1


# In[56]:


d


# At this point you're probably asking yourself, whether to use `**` or `.copy()` to create a shallow copy. We can even create a shallow of one dict by passing the dict to the `dict()` constructor.
# 
# Firstly, the `**` unpacking is more flexible because you can unpack multiple dictionaries into a single new one - `copy` is restricted to copying a single dictionary.
# 
# But what about timings? Is one faster than the other?
# 
# What about using a dictionary comprehension to copy a dictionary? Is that faster/slower?
# 
# Let's try it out and see:

# In[57]:


from random import randint

big_d = {k: randint(1, 100) for k in range(1_000_000)}


# In[58]:


def copy_unpacking(d):
    d1 = {**d}
    
def copy_copy(d):
    d1 = d.copy()

def copy_create(d):
    d1 = dict(d)
    
def copy_comprehension(d):
    d1 = {k: v for k, v in d.items()}


# In[59]:


from timeit import timeit


# In[60]:


timeit('copy_unpacking(big_d)', globals=globals(), number=100)


# In[61]:


timeit('copy_copy(big_d)', globals=globals(), number=100)


# In[62]:


timeit('copy_create(big_d)', globals=globals(), number=100)


# In[63]:


timeit('copy_comprehension(big_d)', globals=globals(), number=100)


# So, creating, unpacking and `.copy()` are about the same - certainly not significant enough to be concerned. A comprehension on the other hand is substantially slower - so, don't use comprehension syntax to do a simple shallow copy!
