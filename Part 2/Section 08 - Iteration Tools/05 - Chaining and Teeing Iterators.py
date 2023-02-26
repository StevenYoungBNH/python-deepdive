#!/usr/bin/env python
# coding: utf-8

# ### Chaining and Teeing Iterators

# Often we need to chain iterators/iterables together to behave like a single iterable.
# 
# We can think of this as analogous to sequence concatenation.
# 
# For example, suppose we have some generators producing squares:

# In[1]:


l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))


# And we want to essentially iterate through all the values as if they were a single iterator.
# 
# We could do it this way:

# In[2]:


for gen in (l1, l2, l3):
    for item in gen:
        print(item)


# In fact, we could even create our own generator function to do this:

# In[3]:


def chain_iterables(*iterables):
    for iterable in iterables:
        yield from iterable


# In[4]:


l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

for item in chain_iterables(l1, l2, l3):
    print(item)


# But, a much simpler way is to use `chain` in the `itertools` module:

# In[5]:


from itertools import chain


# In[6]:


l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

for item in chain(l1, l2, l3):
    print(item)


# Note that `chain` expects a variable number of positional arguments, each of which should be an iterable.
# 
# It will not work if we pass it a single iterable:

# In[7]:


l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

lists = [l1, l2, l3]
for item in chain(lists):
    print(item)


# As you can see, it simply took our list and handed it back directly - there was nothing else to chain with:

# In[8]:


l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

lists = [l1, l2, l3]
for item in chain(lists):
    for i in item:
        print(i)


# Instead, we could use unpacking:

# In[9]:


l1 = (i**2 for i in range(4))
l2 = (i**2 for i in range(4, 8))
l3 = (i**2 for i in range(8, 12))

lists = [l1, l2, l3]
for item in chain(*lists):
    print(item)


# Unpacking works with iterables in general, so even the following would work just fine:

# In[10]:


def squares():
    yield (i**2 for i in range(4))
    yield (i**2 for i in range(4, 8))
    yield (i**2 for i in range(8, 12))


# In[11]:


for item in chain(*squares()):
    print(item)


# But, unpacking is not lazy!! Here's a simple example that shows this, and why we have to be careful using unpacking if we want to preserve lazy evaluation:

# In[12]:


def squares():
    print('yielding 1st item')
    yield (i**2 for i in range(4))
    print('yielding 2nd item')
    yield (i**2 for i in range(4, 8))
    print('yielding 3rd item')
    yield (i**2 for i in range(8, 12))


# In[13]:


def read_values(*args):
    print('finised reading args')


# In[14]:


read_values(*squares())


# Instead we can use an alternate "constructor" for chain, that takes a single iterable (of iterables) and lazily iterates through the outer iterable as well:

# In[15]:


c = chain.from_iterable(squares())


# In[16]:


for item in c:
    print(item)


# Note also, that we can easily reproduce the same behavior of either chain quite easily:

# In[17]:


def chain_(*args):
    for item in args:
        yield from item


# In[18]:


def chain_iter(iterable):
    for item in iterable:
        yield from item


# And we can use those just as we saw before with `chain` and `chain.from_iterable`:

# In[19]:


c = chain_(*squares())


# In[20]:


c = chain_iter(squares())
for item in c:
    print(item)


# ### "Copying" an Iterator

# Sometimes we may have an iterator that we want to use multiple times for some reason.
# 
# As we saw, iterators get exhausted, so simply making multiple references to the same iterator will not work - they will just point to the same iterator object.
# 
# What we would really like is a way to "copy" an iterator and use these copies independently of each other.

# We can use `tee` in `itertools`:

# In[21]:


from itertools import tee


# In[22]:


def squares(n):
    for i in range(n):
        yield i**2


# In[23]:


gen = squares(10)
gen


# In[24]:


iters = tee(squares(10), 3)


# In[25]:


iters


# In[26]:


type(iters)


# As you can see `iters` is a **tuple** contains 3 iterators - let's put them into some variables and see what each one is:

# In[27]:


iter1, iter2, iter3 = iters


# In[28]:


next(iter1), next(iter1), next(iter1)


# In[29]:


next(iter2), next(iter2)


# In[30]:


next(iter3)


# As you can see, `iter1`, `iter2`, and `iter3` are essentially three independent "copies" of our original iterator (`squares(10)`)

# Note that this works for any iterable, so even sequence types such as lists:

# In[31]:


l = [1, 2, 3, 4]


# In[32]:


lists = tee(l, 2)


# In[33]:


lists[0]


# In[34]:


lists[1]


# But you'll notice that the elements of `lists` are not lists themselves!

# In[35]:


list(lists[0])


# In[36]:


list(lists[0])


# As you can see, the elements returned by `tee` are actually `iterators` - even if we used an iterable such as a list to start off with!

# In[37]:


lists[1] is lists[1].__iter__()


# In[38]:


'__next__' in dir(lists[1])


# Yep, the elements of `lists` are indeed iterators!
