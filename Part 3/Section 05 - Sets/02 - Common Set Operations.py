#!/usr/bin/env python
# coding: utf-8

# ### Common Set Operations

# Let's look at some of the more basic and common operations with sets:
# * size
# * membership testing
# * adding elements
# * removing elements

# #### Size

# The size of a set (it's cardinality), is given by the `len()` function - the same one we use for sequences, iterables, dictionaries, etc.

# In[1]:


s = {1, 2, 3}
len(s)


# #### Membership Testing

# This is also very easy:

# In[2]:


s = {1, 2, 3}


# In[3]:


1 in s


# In[4]:


10 in s


# In[5]:


1 not in s


# In[6]:


10 not in s


# But let's go a little further and consider how membership testing works with sets. As I mentioned in earlier lectures, sets are hash tables, and membership testing is **extremely** efficient for sets, since it's simply a hash table lookup - as opposed to scanning a list for example, until we find the requested element (or not).
# 
# Let's do some quick timings to verify this, as well as compare lookup speeds for sets and dictionaries as well (which are also, after all, hash tables).

# In[7]:


from timeit import timeit


# In[8]:


n = 100_000
s = {i for i in range(n)}
l = [i for i in range(n)]
d = {i:None for i in range(n)}


# Let's time how long it takes to find if `9` is in the object - which would be the tenth element only of the list and the dictionary (keys), and who knows for the set:

# In[9]:


number = 1_000_000
search = 9
t_list = timeit(f'{search} in l', globals=globals(), number=number)
t_set = timeit(f'{search} in s', globals=globals(), number=number)
t_dict = timeit(f'{search} in d', globals=globals(), number=number)
print('list:', t_list)
print('set:', t_set)
print('dict:', t_dict)


# The story changes even more if we test for example the last element of the list.
# I'm definitely not to run the tests `1_000_000` times - not unless we want to make this video reaaaaaaly long!

# In[10]:


number = 3_000
search = 99_999
t_list = timeit(f'{search} in l', globals=globals(), number=number)
t_set = timeit(f'{search} in s', globals=globals(), number=number)
t_dict = timeit(f'{search} in d', globals=globals(), number=number)
print('list:', t_list)
print('set:', t_set)
print('dict:', t_dict)


# The situation for `not in` is the same:

# In[11]:


number = 3_000
search = -1
t_list = timeit(f'{search} not in l', globals=globals(), number=number)
t_set = timeit(f'{search} not in s', globals=globals(), number=number)
t_dict = timeit(f'{search} not in d', globals=globals(), number=number)
print('list:', t_list)
print('set:', t_set)
print('dict:', t_dict)


# But this efficiency does come at the cost of memory:

# In[12]:


print(d.__sizeof__())
print(s.__sizeof__())
print(l.__sizeof__())


# Even for empty objects:

# In[13]:


s = set()
d = dict()
l = list()


# In[14]:


print(d.__sizeof__())
print(s.__sizeof__())
print(l.__sizeof__())


# And adding just one element to each object:

# In[15]:


s.add(10)
d[10] =None
l.append(10)


# In[16]:


print(d.__sizeof__())
print(s.__sizeof__())
print(l.__sizeof__())


# If you're wondering why the dictionary and set size did not increase, remember when we covered hash tables - there is some overallocation that takes place so we don't incure the cost of resizing every time we had an element. In fact, lists do the same as well - they over-allocate to reduce the resizing cost. I'll come back to that in a minute.

# #### Adding Elements

# When we have an existing set, we can always add elements to it. Of course *where* it gets "inserted" is unknown. So Python does not call it `append` or `insert` which would connotate ordering of some kind - instead it just calls it `add`:

# In[17]:


s = {30, 20, 10}


# In[18]:


s.add(15)


# In[19]:


s


# Don't be fooled by the apparent ordering of the elements here. This is the same as with dictionaries - Jupyter tries to represent things nicely for us, but underneath the scenes:

# In[20]:


print(s)


# In[21]:


s.add(-1)
print(s)


# And the order just changed again! :-)

# What's interesting about the `add()` method, is that if we try to add an element that already exists, Python will simply ignore it:

# In[22]:


s


# In[23]:


s.add(15)


# In[24]:


s


# Now that we know how to add an element to a set, let's go back and see how  the set, dictionary and list resize as we add more elements to them.
# We should expect the list to be more efficient from a memory standpoint:

# In[25]:


l = list()
s = set()
d = dict()

print('#', 'dict', 'set', 'list')
for i in range(50):
    print(i, d.__sizeof__(), s.__sizeof__(), l.__sizeof__())
    l.append(i)
    s.add(i)
    d[i] = None


# As you can see, the memory costs for a set or a dict are definitely higher than for a list. You can also see from this how it looks like CPython implements different resizing strategies for sets, dicts and lists.
# The strategy by the way has nothing to do with the size of the elements we put in those objects:

# In[26]:


l = list()
s = set()
d = dict()

print('#', 'dict', 'set', 'list')
for i in range(50):
    print(i, d.__sizeof__(), s.__sizeof__(), l.__sizeof__())
    l.append(i**1000)
    s.add(i*1000)
    d[i*1000] = None


# As you can see the memory cost of the objects themselves did not change, nor did the sizing strategy (remember that all those objects contain pointers to the data, not the data itself - and a pointer to an object, no matter the size of that object, is the same).
# So be careful using `__sizeof__` - it's often only part of the story.

# #### Removing Elements

# Now let's see how we can remove elements from a set.
# 
# Just as with dictionaries, we may be trying to remove an item that does not exist in the set. Depending on whether we want to silently ignore deletion of non-existent elements we can use one of two techniques:

# In[27]:


s = {1, 2, 3}


# In[28]:


s.remove(1)


# In[29]:


s


# In[30]:


s.remove(10)


# As you can see, we get an exception.
# 
# If we don't want the exception we can do it this way:

# In[31]:


s.discard(10)


# In[32]:


s


# We can also remove (and return) an **arbitrary** element from the set:

# In[33]:


s = set('python')


# In[34]:


s


# In[35]:


s.pop()


# Note that we **do not know** ahead of time what element will get popped.
# 
# Also, popping an empty set will result in a `KeyError` exception:

# In[36]:


s = set()
s.pop()


# Something like that might be handy to handle all the elements of a set one at a time without caring for the order in which elements are removed from the set - not that you can, anyway - sets are not ordered!
# But this way you can get at the elements of a set without knowing the content of the set (since you need to know the element you are removing with `remove` and `discard`.)

# Finally, you can empty out a set by calling the `clear` method:

# In[37]:


s = {1, 2, 3}
s.clear()
s

