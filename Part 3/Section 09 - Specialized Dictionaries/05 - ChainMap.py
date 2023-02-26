#!/usr/bin/env python
# coding: utf-8

# ### ChainMap

# Remember the `chain` function in the `itertools` module? That allowed us to chain multiple iterables together to look like a single iterable.
# 
# The `ChainMap` in the `collections` module is somewhat similar - it allows us to chain multiple dictionaries (mapping types more generally) so it looks like a single mapping type.
# But there are some wrinkles: 
# * when we request a key lookup, what happens if the same key occurs in more than one dictionary?
# * we can actually update, insert and delete elements from a ChainMap - how does that work?

# Let's look at some simple examples where we do not have key collisions first:

# In[1]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'e': 5, 'f': 6}


# Now we can always create a new dictionary that contains all those keys by using unpacking, or even starting with an empty dictionary and updating it three times with each of the dicts `d1, d2` and `d3`:

# In[2]:


d = {**d1, **d2, **d3}


# In[3]:


print(d)


# or:

# In[4]:


d = {}
d.update(d1)
d.update(d2)
d.update(d3)


# In[5]:


print(d)


# But in a way this is wasteful because we had to copy the data into a new dictionary.
# 
# Instead we can use `ChainMap`:

# In[6]:


from collections import ChainMap


# In[7]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'e': 5, 'f': 6}
d = ChainMap(d1, d2, d3)


# In[8]:


print(d)


# In[9]:


isinstance(d, dict)


# So, the result is not a dictionary, but it is a mapping type that we can use almost **like** a dictionary:

# In[10]:


d['a']


# In[11]:


d['c']


# In[12]:


for k, v in d.items():
    print(k, v)


# **Note** that the iteration order here, unlike a regular Python dictionary, is **not** guaranteed!

# Now what happens if we have key 'collisions'?

# In[13]:


d1 = {'a': 1, 'b': 2}
d2 = {'b': 20, 'c': 3}
d3 = {'c': 30, 'd': 4}


# In[14]:


d = ChainMap(d1, d2, d3)


# In[15]:


d['b']


# In[16]:


d['c']


# As you can see, the value returned corresponds to the the value of the **first** key found in the chain. (So note the difference between this and when we unpack the dictionaries into a new dictionary, where the "last" key effectively overwrite any "previous" key.)
# 
# In fact, if we iterate through all the items, you'll notice that, as we would expect from a mapping type, we do not have duplicate keys, and moreover the associated value is the **first** one encountered in the chain:

# In[17]:


for k, v in d.items():
    print(k, v)


# Now let's look at how ChainMap objects handle inserts, deletes and updates:

# In[18]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'e': 5, 'f': 6}
d = ChainMap(d1, d2, d3)


# In[19]:


d['z'] = 100


# In[20]:


print(d)


# As you can see the element `'z': 100` was added to the chain map. But what about the underlying dictionaries that make up the map?

# In[21]:


print(d1)
print(d2)
print(d3)


# When mutating a chain map, the **first** dictionary in the chain is used to handle the mutation - even updates:

# Let's try to update `c`, which is in the second dictionary:

# In[22]:


d['c'] = 300


# In[23]:


print(d)


# As you can see the **first** dictionary in the chain was "updated" - since the key did not exist, the key with the "updated" value was added to the underlying dictionary:

# In[24]:


print(d1)
print(d2)
print(d3)


# As you can see, a **new** element `c` was created in the **first** dict in the chain. When we view it from the chain map perspective, it looks like `c` was updated because it was actually inserted in the first dict, so that key is encountered in that dict first, and hence that new value is used.

# What about deleting an item?

# In[25]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'e': 5, 'f': 6}
d = ChainMap(d1, d2, d3)


# In[26]:


del d['a']


# In[27]:


list(d.items())


# In[28]:


print(d1)
print(d2)
print(d3)


# As you can see `a` was deleted from the first dict.

# Something important to note here when deleting keys, is that deleting a key does not guarantee the key no longer exists in the chain! It could exist in one of the parents, and only the child is affected:

# In[29]:


d1 = {'a': 1, 'b': 2}
d2 = {'a': 100}
d = ChainMap(d1, d2)


# In[30]:


d['a']


# In[31]:


del d['a']


# In[32]:


d['a']


# Since we can only mutate the **first** dict in the chain, trying to delete an item that is present in the chain, but not in the child will cause an exception:

# In[33]:


del d['c']


# A `ChainMap` is built as a view on top of a sequence of mappings, and those maps are incorporated **by reference**.
# This means that if an underlying map is mutated, then the `ChainMap` instance will **see** the change:

# In[34]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'e': 5, 'f': 6}
d = ChainMap(d1, d2, d3)


# In[35]:


list(d.items())


# In[36]:


d3['g'] = 7


# In[37]:


list(d.items())


# We can even chain ChainMaps.
# For example, we can use this approach to "append" a new dictionary to a chain map, in essence create a **new** chain map containing the maps from one chain map and adding one or more maps to the list:

# In[38]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d = ChainMap(d1, d2)


# In[39]:


d3 = {'d':400, 'e': 5 }
d = ChainMap(d, d3)


# In[40]:


print(d)


# Of course, we could place `d3` in front:

# In[41]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d = ChainMap(d1, d2)


# In[42]:


d3 = {'d':400, 'e': 5 }
d = ChainMap(d3, d)
print(d)


# So the ordering of the maps in the chain matters!

# Instead of adding an element to the beginning of the chain list using the technique above, we can also use the `new_child` method, which returns a new chain map with the new element added to the beginning of the list:

# In[43]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d = ChainMap(d1, d2)


# In[44]:


d3 = {'d':400, 'e': 5 }
d = d.new_child(d3)
print(d)


# And as you can see the key `d: 400` is in our chain map.

# There is also a property that can be used to return every map in the chain **except** the first map:

# In[45]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d3 = {'e': 5, 'f': 6}
d = ChainMap(d1, d2, d3)
print(d)


# In[46]:


d = d.parents
print(d)


# The chain map's list of maps is accessible via the `maps` property:

# In[47]:


d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}
d = ChainMap(d1, d2)


# In[48]:


type(d.maps), d.maps


# As you can see this is a list, and so we can actually manipulate it as we would any list:

# In[49]:


d3 = {'e': 5, 'f': 6}
d.maps.append(d3)


# In[50]:


d.maps


# We could equally well remove a map from the list entirely, insert one wherever we want, etc:

# In[51]:


d.maps.insert(0, {'a': 100})


# In[52]:


d.maps


# In[53]:


print(list(d.items()))


# As you can see `a` now has a value of `100` in the chain map.

# We can also delete a map from the chain entirely:

# In[54]:


del d.maps[1]


# In[55]:


d.maps


# ##### Example

# A typical application of a chain map, apart from "merging" multiple dictionaries without incurring extra overhead copying the data, is to create a mutable version of merged dictionaries that does not mutate the underlying dictionaries.
# 
# Remember that mutating elements of a chain map mutates the elements of the first map in the list only.

# Let's say we have a dictionary with some settings and we want to temporarily modify these settings, but without modifying the original dictionary.
# 
# We could certainly copy the dictionary and work with the copy, discarding the copy when we no longer need it - but again this incurs some overhead copying all the data.
# 
# Instead we can use a chain map this way, by making the first dictionary in the chain a new empty dictionary - any updates we make will be made to that dictionary only, thereby preserving the other dictionaries.

# In[56]:


config = {
    'host': 'prod.deepdive.com',
    'port': 5432,
    'database': 'deepdive',
    'user_id': '$pg_user',
    'user_pwd': '$pg_pwd'
}


# In[57]:


local_config = ChainMap({}, config)


# In[58]:


list(local_config.items())


# And we can make changes to `local_config`:

# In[59]:


local_config['user_id'] = 'test'
local_config['user_pwd'] = 'test'


# In[60]:


list(local_config.items())


# But notice that our original dictionary is unaffected:

# In[61]:


list(config.items())


# That's because the changes we made were reflected in the **first** dictionary in the chain - that empty dictionary:

# In[62]:


local_config.maps

