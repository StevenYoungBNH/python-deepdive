#!/usr/bin/env python
# coding: utf-8

# ### Views: keys, values and items

# We'll come back to these dictionary views in a lot more detail once we have studied sets, because they are very related.
# 
# For now, let's just briefly look at the basics of these views.

# Views are special objects that support set behavior and also support iteration over the keys, values, and key/value pairs (items) in a dictionary.

# A quick look at some common set operations:

# In[1]:


s1 = {1, 2, 3}
s2 = {2, 3, 4}


# Unions:

# In[2]:


s1 | s2


# Intersections:

# In[3]:


s1 & s2


# Differences:

# In[4]:


s1 - s2


# In[5]:


s2 - s1


# Now let's look at these views:

# In[6]:


d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'c': 30, 'd': 4, 'e': 5}


# We can iterate over the keys of a dictionary using the dictionary's iterator directly, or via the `keys` view:

# In[7]:


for key in d1:
    print(key)


# In[8]:


for key in d1.keys():
    print(key)


# We can iterate over just the values of the dictionary:

# In[9]:


for value in d1.values():
    print(value)


# and over the items, as tuples, of the dictionary:

# In[10]:


for item in d1.items():
    print(item)


# We can also unpack the tuples directly while iterating:

# In[11]:


for k, v in d1.items():
    print(k, v)


# These views are iterables, not just iterators:

# In[12]:


keys = d1.keys()


# In[13]:


list(keys)


# In[14]:


list(keys)


# As you can see we can iterate over and over on the same view.

# The order in which keys, value and items are returned during iteration match - as long as the dictionary has not changed in-between.
# 
# So for example, the following expression will always evaluate to true:

# In[15]:


list(d1.items()) == list(zip(d1.keys(), d1.values()))


# Views are dynamic, in the sense that if something changes in the dictionary, the views immediately reflect the change - that's because the views do not themselves contain data, they simply have extra bits of functionality that uses the dictionary as the source of truth.

# In[16]:


keys


# In[17]:


d1['z'] = 10


# In[18]:


keys


# In[19]:


del d1['z']


# In[20]:


keys


# Now, the interesting thing is that some of these views also exhibit set behaviors.

# In[21]:


print(d1)
print(d2)


# We can find all the keys that are in both `d1` and `d2`:

# In[22]:


print(type(d1.keys()), d1.keys())
print(type(d2.keys()), d2.keys())
union = d1.keys() | d2.keys()
print(type(union), union)


# One thing to really watch out for here: once we start performing set like operations, the result is a true `set`, and although ordering in the views is guaranteed, ordering in the resulting sets are **not** as you can see from the example above!

# We can also find the keys that are in both `d1` and `d2`:

# In[23]:


d1.keys() & d2.keys()


# We can also find the keys that are only in `d1` but not in `d2`:

# In[24]:


d1.keys() - d2.keys()


# The same works with items as well:

# In[25]:


d1.items() | d2.items()


# You'll notice that `('c', 3)` and `('c', 30)` are distinct elements, hence they show up as individual elements in the result.

# Values on the other hand are more problematic. Keys in a dictionary must be hashable, and set elements must also be hashable, so it's not a problem creating a set of keys for example. But what about values? These need noe be unique or hashable. And items for that matter? The first element of the tuple must be hashable since it's the key, but the value?

# In[26]:


d3 = {'a': [1, 2], 'b': [3, 4]}
d4 = {'b': [30, 40], 'c': [5, 6]}


# In[27]:


d3.values()


# Can we perform some set operations on the values?

# In[28]:


d3.values() | d4.values()


# The answer is no, the `values` view does not behave like a set - it can't because there is no guarantee the values are unique and hashable.

# What's interesting though is that `items` does have unique values (since the keys are unique), but the values may or may not be hashable as in the example of `d3` and `d4`:

# In[29]:


print(d3)
print(d4)


# In[30]:


d3.items() | d4.items()


# As you can see, `items`, in this case also does not exhibit set like capabilities.
# 
# But that's not always the case. Let's go back to our first example:

# In[31]:


print(d1)
print(d2)


# In[32]:


d1.items() | d2.items()


# Aha! In this case `items` **does** behave like a set - that's because the values are all hashable!

# That's all I'm going to cover for now on dictionary views, we'll come back to them in greater detail in the context of sets.

# ##### Example 1

# Let's take a look at a practical example of using these views for something other than plain iteration:

# Let's say we have two dictionaries, and we want to create a new dictionary that contains all the items whose keys are in both dictionaries.
# We want the value in the new dictionary to be a tuple containing all the values from both dictionaries:

# In[33]:


d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 2, 'c': 30, 'd': 4}


# In[34]:


k1 = d1.keys()
k2 = d2.keys()
k1 & k2


# So we have now identified the common keys, all that's left to do is build a dictionary from those keys and the corresponding values.
# 
# We can use a simple loop to do this:

# In[35]:


new_dict = {}
for key in d1.keys() & d2.keys():
    new_dict[key] = (d1[key], d2[key])
print(new_dict)


# But, a dictionary comprehension would be a better approach here:

# In[36]:


new_dict = {key: (d1[key], d2[key]) for key in d1.keys() & d2.keys()}
print(new_dict)


# ##### Example 2

# Let's tweak this a bit and generate a new dictionary, again containing just the common keys, but whose value is either the common value, or if the underlying dictionaries have different values for the same key, choose the values from the second dictionary, discarding the values from the first.

# The approach is going to be almost identical to the previous example.
# 
# Let's just see which value we want to use for both cases (same values, different values):
# * same values: pick value from `d1` or `d2` (since values are the same it does not matter)
# * different values: pick value from `d2`
# 
# As you can see, in both cases we just need to pick the value in `d2`.

# In[37]:


d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 2, 'c': 30, 'd': 4}
new_dict = {key: d2[key] for key in d1.keys() & d2.keys()}
print(new_dict)


# ##### Example 3

# For this example, suppose we have two dictionaries, and we want to identify items whose keys are **not** common to both dictionaries:

# In[38]:


d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d2 = {'a': 10, 'b': 20, 'c': 30, 'e': 5}


# As you can see from visual inspection, we want to end up with a dictionary that looks like this:

# In[39]:


{'d': 4, 'e': 5}


# First let's consider how we would identify the non-common keys.
# 
# Start with the union of the keys - this identifies all unique keys in both dictionaries:

# In[40]:


union = d1.keys() | d2.keys()
print(union)


# Next, we look at the intersection of the keys - this identifies all keys common to both dictionaries:

# In[41]:


intersection = d1.keys() & d2.keys()
print(intersection)


# Finally, we can remove the keys in the intersection from the kesy in the union:

# In[42]:


keys = union - intersection
print(keys)


# As you can see we now have the keys we are interested in.
# All that's left is to pick up the values as well.
# 
# (We'll cover this later in the section on sets, but there's a quicker way to get this, using something called a symmetric difference.)
# 
# First note that given a key, it will be present in either `d1` or `d2`, but not both.
# So to get the value for the key we need to look at both dictionaries and pick the value from whichever dictionary has the key:

# In[43]:


value = d1.get('e')
print(value)


# In[44]:


value = d2.get('e')
print(value)


# So, we can combine these two expressions with an or to get the non-`None` value (one of them always will be `None`):

# In[45]:


d1.get('d') or d2.get('d')


# In[46]:


d1.get('e') or d2.get('e')


# So now we need to use this to gather up the values for our keys and create a result dictionary:

# We could do it using a standard loop:

# In[47]:


d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d2 = {'a': 10, 'b': 20, 'c': 30, 'e': 5}
union = d1.keys() | d2.keys()
intersection = d1.keys() & d2.keys()
keys = union - intersection

result = {}
for key in keys:
    result[key] = d1.get(key) or d2.get(key)
print(result)


# Or, better yet, we could use a dictionary comprehension:

# In[48]:


result = {key: d1.get(key) or d2.get(key) for key in keys}
print(result)


# Just for completeness, and again, we'll cover this in detail later, we can use the symmetric difference operator for sets (`^`) which does in one operation the same thing we did with the union, intersection, and difference operators, making this even more concise:

# In[49]:


d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d2 = {'a': 10, 'b': 20, 'c': 30, 'e': 5}
result = {key: d1.get(key) or d2.get(key)
         for key in d1.keys() ^ d2.keys()}
print(result)

