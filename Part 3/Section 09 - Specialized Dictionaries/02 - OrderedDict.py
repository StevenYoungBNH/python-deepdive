#!/usr/bin/env python
# coding: utf-8

# ### OrderedDict

# Prior to Python 3.7, dictionary key order was not guaranteed. This became part of the language in 3.7, so the usefullness of this `OrderedDict` is diminished - but necessary if you want your dictionaries to maintain key order **and** be compatible with Python versions earlier then 3.6 (technically dicts are ordered in 3.6 as well, but it was considered an implementation detail, and not actually guaranteed).

# We'll come back to a direct comparison of `OrderedDict` and plain `dict` in a subsequent video. For now let's look at the `OrderedDict` as if we were targeting our code to be compatible with earlier versions of Python.

# In[1]:


from collections import OrderedDict


# Once again, `OrderedDict` is a subclass of `dict`.
# 
# We can also pass keyword arguments to the constructor. However, in Python versions prior to 3.5, the order of the arguments is not guaranteed to be preserved - so to be fully backward-compatible, insert keys into the dictionary **after** you have created it as an empty dictionary.

# Let's try it out:

# In[2]:


d = OrderedDict()


# In[3]:


d['z'] = 'hello'


# In[4]:


d['y'] = 'world'


# In[5]:


d['a'] = 'python'


# In[6]:


d


# And if we iterate through the keys of the `OrderedDict` we will retain that key order as well:

# In[7]:


for key in d:
    print(key)


# The `OrderedDict` also supports reverse iteration using `reversed()`:

# In[8]:


for key in reversed(d):
    print(key)


# This is not the case for a standard dictionary, even in Python 3.5+ where key order is maintained!
# 
# In the next video we'll dig a little more into a comparison between `OrderedDicts` and `dicts`.

# In[9]:


d = {'a': 1, 'b': 2}
for key in reversed(d):
    print(key)


# `OrderedDicts` are a subclass of `dicts` so all the usual operations and methods apply, but `OrderedDicts` have a couple of extra methods available to us:
# 1. `popitem(last=True)`
# 2. `move_to_end(key, last=True)`

# Since an `OrderedDict` has an ordering, it is natural to think of the *first* or *last* element in the dictionary.
# 
# The `popitem` allows us to remove the last (by default) or first item (setting `last=False`):

# In[10]:


d = OrderedDict()
d['first'] = 10
d['second'] = 20
d['third'] = 30
d['last'] = 40


# In[11]:


d


# In[12]:


d.popitem()


# In[13]:


d


# As you can see the last item was popped off (and returned as a key/value tuple). To pop the first item we can do this:

# In[14]:


d.popitem(last=False)


# In[15]:


d


# The `move_to_end` method simply moves the specified key to the end (by default), or to the beginning (if `last=False` is specified) of the dictionary:

# In[16]:


d = OrderedDict()
d['first'] = 10
d['second'] = 20
d['third'] = 30
d['last'] = 40


# In[17]:


d.move_to_end('second')


# In[18]:


d


# In[19]:


d.move_to_end('third', last=False)


# In[20]:


d


# Be careful if you specify a non-existent key, you will get an exception:

# In[21]:


d.move_to_end('x')


# #### Equality Comparisons

# With regular dictionaries, two dictionaries are considered equal (`==`) if they contain the same key/value pairs, irrespective of the ordering.

# In[22]:


d1 = {'a': 10, 'b': 20}
d2 = {'b': 20, 'a': 10}


# In[23]:


d1 == d2


# But this is not the case with `OrderedDicts` - since ordering matters here, two `OrderedDicts` will compare equal if both their key/values pairs are equal **and** if the keys are in the same order:

# In[24]:


d1 = OrderedDict()
d1['a'] = 10
d1['b'] = 20

d2 = OrderedDict()
d2['a'] = 10
d2['b'] = 20

d3 = OrderedDict()
d3['b'] = 20
d3['a'] = 10


print(d1)
print(d2)
print(d3)


# In[25]:


d1 == d2


# In[26]:


d1 == d3


# Now, an `OrderedDict` is a subclass of a standard `dict`:

# In[27]:


isinstance(d1, OrderedDict)


# In[28]:


isinstance(d1, dict)


# So, can we compare an `OrderedDict` with a plain `dict`?
# 
# The answer is yes, and in this case order does **not** matter:

# In[29]:


d1 = OrderedDict()
d1['a'] = 10
d1['b'] = 20

d2 = {'b': 20, 'a': 10}

print(d1)
print(d2)


# In[30]:


d1 == d2


# In[31]:


d2 == d1


# #### Using an OrderedDict as a Stack or Queue

# If you are familiar with stacks and queues, you are probably wondering if the `popitem` method means we can effectively use an `OrderedDict` as such data structures.
# 
# Well yes, we can, but the real question is whether it is as efficient as using a `deque` for example.
# 
# Let's try it out and do some timings:

# In[32]:


from timeit import timeit


# In[33]:


from collections import deque


# In[34]:


def create_ordereddict(n=100):
    d = OrderedDict()
    for i in range(n):
        d[str(i)] = i
    return d


# In[35]:


def create_deque(n=100):
    return deque(range(n))   


# Now let's time how log it takes to pop off the last element of each data structure repeatedely until the structure is empty.
# 
# Instead of testing each time if the structure is empty, I'm going to simply pop items until I get an exception - since I only expect one exception and many many more succesful pop attempts, this will be more efficient:

# A `deque` will raise an `IndexError` exception if we attempt to pop an item from an empty `deque`. The `OrderedDict` will raise a `KeyError` exception.

# In[36]:


def pop_all_ordered_dict(n=1000, last=True):
    d = create_ordereddict(n)
    while True:
        try:
            d.popitem(last=last)
        except KeyError:
            # done popping
            break           


# In[37]:


def pop_all_deque(n=1000, last=True):
    dq = create_deque(n)
    if last:
        pop = dq.pop
    else:
        pop = dq.popleft

    while True:
        try:
            pop()
        except IndexError:
            break


# Now let's go ahead and time these operations, both the creations and the pops:

# In[38]:


timeit('create_ordereddict(10_000)', 
       globals=globals(), 
       number=1_000)


# In[39]:


timeit('create_deque(10_000)', 
       globals=globals(), 
       number=1_000)


# Now let's time popping elements - keep in mind that we are also timing the recreation of the data structures every time as well - so our timings are going to be biased because of that. A very rough way of rectifying that will be to subtract how much time we measured above for creating the structures by themselves:

# In[40]:


n = 10_000
number = 1_000

results = dict()

results['dict_create'] = timeit('create_ordereddict(n)', 
                                globals=globals(), 
                                number=number)

results['deque_create'] = timeit('create_deque(n)', 
                                 globals=globals(), 
                                 number=number)

results['dict_create_pop_last'] = timeit(
    'pop_all_ordered_dict(n, last=True)',
    globals=globals(), number=number)

results['dict_create_pop_first'] = timeit(
    'pop_all_ordered_dict(n, last=False)',
    globals=globals(), number=number)

results['deque_create_pop_last'] = timeit(
    'pop_all_deque(n, last=True)',
    globals=globals(), number=number
)

results['deque_create_pop_first'] = timeit(
    'pop_all_deque(n, last=False)',
    globals=globals(), number=number
)

results['dict_pop_last'] = (
    results['dict_create_pop_last'] - results['dict_create'])

results['dict_pop_first'] = (
    results['dict_create_pop_first'] - results['dict_create'])

results['deque_pop_last'] = (
    results['deque_create_pop_last'] - results['deque_create'])

results['deque_pop_first'] = (
    results['deque_create_pop_first'] - results['deque_create'])

for key, result in results.items():
    print(f'{key}: {result}')


# As you can see, even though we can certainly use an `OrderedDict` as a stack or queue (and there might be good reasons why we want to use a dictionary for such structures), if you can use a `deque` you will get much faster performance.
# 
# One good reason might be if you both need a stack/queue and also need to check for the existence of items frequently - searching a list is very inefficient compared to a dictionary, so depending on your use case the cost of looking up items in a `deque` might be worth the cost of popping/inserting items in an `OrderedDict` instead.
