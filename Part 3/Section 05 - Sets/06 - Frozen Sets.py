#!/usr/bin/env python
# coding: utf-8

# ### Frozen Sets

# `frozenset` is the **immutable** equivalent of the plain `set`.
# 
# Apart from the fact that you cannot mutate the collection (i.e. add or remove elements), the interesting thing is that frozen sets are hashable (as long as each contained element is also hashable).
# 
# This means that whereas we cannot create a set of sets, we can create a set of frozen sets (or a frozen set of frozen sets). It also means that we can use frozen sets as dictionary keys.
# 
# There is no literal for frozen sets - we have to use the `frozenset()` callable. It is used the same way to create frozensets that `set()` would be used to create sets.

# In[1]:


s1 = {'a', 'b', 'c'}


# In[2]:


hash(s1)


# In[3]:


s2 = frozenset(['a', 'b', 'c'])


# In[4]:


hash(s2)


# And we can create a set of frozen sets:

# In[5]:


s3 = {frozenset({'a', 'b'}), frozenset([1, 2, 3])}


# In[6]:


s3


# #### Copying Frozen Sets

# Remember what happens when we create a shallow copy of a tuple using the `tuple()` callable?

# In[7]:


t1 = (1, 2, [3, 4])


# In[8]:


t2 = tuple(t1)


# In[9]:


t1 is t2


# This is quite different from what happens with a list:

# In[10]:


l1 = [1, 2, [3, 4]]
l2 = list(l1)


# In[11]:


l1 is l2


# Remember that there's really no point in making a shallow copy of an immutable container - so, Python optimizes this for us and just returns the original tuple. Of course, lists are mutable, and that optimization cannot happen.
# 
# The same thing happens with sets and frozen sets:

# In[12]:


s1 = {1, 2, 3}
s2 = set(s1)
s1 is s2


# In[13]:


s1 = frozenset([1, 2, 3])
s2 = frozenset(s1)
print(type(s1), type(s2), s1 is s2)


# Same goes with the `copy()` method:

# In[14]:


s2 = s1.copy()
print(type(s1), type(s2), s1 is s2)


# Of course, this will not happen with a deep copy in general:

# In[15]:


from copy import deepcopy


# In[16]:


s2 = deepcopy(s1)
print(type(s1), type(s2), s1 is s2)


# #### Set Operations

# All the non-mutating set operations we studied with sets also apply to frozen sets.
# 
# But, in addition, we can mix sets and frozen sets when performing these operations.
# 
# For example:

# In[17]:


s1 = frozenset({'a', 'b'})
s2 = {1, 2}
s3 = s1 | s2


# In[18]:


s3


# What's important to note here is the data type of the result - it is a frozen set.
# Let's do this operation again, but switch around `s1` and `s2`:

# In[19]:


s3 = s2 | s1


# In[20]:


s3


# As you can see, the result is now a standard set.
# 
# Basically the data type of the first operand determines the data type of the result.

# In[21]:


s1 = frozenset({'a', 'b', 'c'})
s2 = {'c', 'd', 'e'}


# In[22]:


s1 & s2


# In[23]:


s2 & s1


# Same goes with differences and symmetric differences:

# In[24]:


s1 - s2


# In[25]:


s2 - s1


# In[26]:


s1 ^ s2


# In[27]:


s2 ^ s1


# What about equality?

# In[28]:


s1 = {1, 2}
s2 = frozenset(s1)


# In[29]:


s1 is s2


# In[30]:


s1 == s2


# As you can see, this is very similar behavior to numerical values:

# In[31]:


1 == 1.0


# In[32]:


1 == 1 + 0j


# Even though they are not the same data type (and hence cannot possibly be the same object), equality still works "as expected".

# ##### Application 1

# One application of frozen sets, assuming they are hashable, is as keys for a dictionary.
# 
# Recall an example we worked on in the past where we wanted a `Person` object to be used as a key in a dictionary.
# 
# We had to define the class, equality and the hash - that was quite a bit of work for what amounted to, in the end just checking that the name and age were the same.
# 
# Of course, we may have more complex instances of this, but for a simple case like that, especially if we consider our `Person` class to be immutable, it would have been easier to just use a frozen set containing the name and age:

# In[33]:


class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
        
    def __repr__(self):
        return f'Person(name={self._name}, age={self._age})'
    
    @property
    def name(self):
        return self._name
        
    @property
    def age(self):
        return self._age
    
    def key(self):
        return frozenset({self.name, self.age})


# In[34]:


p1 = Person('John', 78)
p2 = Person('Eric', 75)


# In[35]:


d = {p1.key(): p1, p2.key(): p2}


# In[36]:


d


# And we can easily lookup using those keys now:

# In[37]:


d[frozenset({'John', 78})]


# In[38]:


d[frozenset({78, 'John'})]


# Of course this is kind of a limited use case, but in the event you have the need to use sets as dictionary keys, then you technically can using a frozen set (as long as the elements are all hashable).

# ##### Application 2

# A slightly more interesting application of this is memoization. I cover memoization in detail in Part 1 of this series in the section on decorators.

# Recall that memoization is basically a technique to cache the results of a (deterministic) function call based on the provided arguments. A cache is created that contains the results of calling the function with a particular set of arguments, the next time the function is called, the arguments are checked against the cache - if the arguments exist in the cache, then the cached value is returned instead of re-executing the function.
# 
# Although Python's `functools` has the `lru_cache` decorator available, there is one drawback - the order of the keyword arguments matters.
# 
# Let's see this:

# In[39]:


from functools import lru_cache


# In[40]:


@lru_cache()
def my_func(*, a, b):
    print('calculating a+b...')
    return a + b


# In[41]:


my_func(a=1, b=2)


# In[42]:


my_func(a=1, b=2)


# Notice how the second time around, we did not see `calculating a+b...` printed out - that's because the value was pulled from cache.
# 
# But now look at this:

# In[43]:


my_func(b=2, a=1)


# Even though the values are technically the same, the order in which we specified them as different, and the cache considered the arguments to be different. Now of course, both "styles" are cached:

# In[44]:


my_func(a=1, b=2)
my_func(b=2, a=1)


# An interesting side note, now that we know all about hashability!
# You'll notice that the way `my_func` works we can actually pass in other data types than just numbers. We could use strings, tuples, even lists or sets:

# In[45]:


my_func(a='abc', b='def')


# In[46]:


my_func(a='abc', b='def')


# As you can see caching works just fine.
# But what is being used to back the cache for `lru_cache`? A dictionary...
# And what do we know about dictionary keys? They must be hashable!
# 
# So this will actually fail, and not because the function can't handle it, but because the `lru_cache` mechanism cannot:

# In[47]:


my_func(a=[1, 2, 3], b=[4, 5, 6])


# Let's write our own version of this.
# We'll use a dictionary to cache the arguments - so we'll need to come up with a key representing the arguments - and one in which the order of the keyword-only arguments does not matter. We'll have the same limitation in terms of hashable keys as `lru_cache`, but at least we won't have the argument ordering issue:

# In[48]:


def memoizer(fn):
    cache = {}
    def inner(*args, **kwargs):
        key = (*args, frozenset(kwargs.items()))
        if key in cache:
            return cache[key]
        else:
            result = fn(*args, **kwargs)
            cache[key] = result
            return result
    return inner


# In[49]:


@memoizer
def my_func(*, a, b):
    print('calculating a+b...')
    return a + b


# In[50]:


my_func(a=1, b=2)


# In[51]:


my_func(a=1, b=2)


# So far so good... Now let's swap the arguments around:

# In[52]:


my_func(b=2, a=1)


# Yay!! It used the cache!

# We can even tweak this to effectively provide more efficient caching when the order of positional arguments is not important either:

# In[53]:


def memoizer(fn):
    cache = {}
    def inner(*args, **kwargs):
        key = frozenset(args) | frozenset(kwargs.items())
        if key in cache:
            return cache[key]
        else:
            result = fn(*args, **kwargs)
            cache[key] = result
            return result
    return inner


# In[54]:


@memoizer
def adder(*args):
    print('calculating...')
    return sum(args)


# In[55]:


adder(1, 2, 3)


# In[56]:


adder(3, 2, 1)


# In[57]:


adder(2, 1, 3)


# In[58]:


adder(1, 2, 3, 4)


# In[59]:


adder(4, 2, 1, 3)


# Isn't Python fun!!
