#!/usr/bin/env python
# coding: utf-8

# ### Sequence Types

# Sequence types have the general concept of a first element, a second element, and so on. Basically an ordering of the sequence items using the natural numbers. In Python (and many other languages) the starting index is set to `0`, not `1`.
#
# So the first item has index `0`, the second item has index `1`, and so on.

# Python has built-in mutable and immutable sequence types.

# Strings, tuples are immutable - we can access but not modify the **content** of the **sequence**:

# In[1]:


t = (1, 2, 3)


# In[2]:


t[0]


# In[3]:


# t[0] = 100


# But of course, if the sequence contains mutable objects, then although we
# cannot modify the sequence of elements (cannot replace, delete or insert elements),
# we certainly **can** change the contents of the mutable objects:

# In[4]:


t = ([1, 2], 3, 4)


# `t` is immutable, but its first element is a mutable object:

# In[5]:


t[0][0] = 100


# In[6]:


t


# #### Iterables

# An **iterable** is just something that can be iterated over, for example using a `for` loop:

# In[7]:


t = (10, 'a', 1 + 3j)


# In[8]:


s = {10, 'a', 1 + 3j}


# In[9]:


for c in t:
    print(c)


# In[10]:


for c in s:
    print(c)


# Note how we could iterate over both the tuple and the set. Iterating the tuple
# preserved the **order** of the elements in the tuple, but not for the set.
# Sets do not have an ordering of elements - they are iterable, but not sequences.

# Most sequence types support the `in` and `not in` operations. Ranges do too,
# but not quite as efficiently as lists, tuples, strings, etc.

# In[11]:


print('a' in ['a', 'b', 100])


# In[12]:


print(100 in range(200))


# #### Min, Max and Length

# Sequences also generally support the `len` method to obtain the number of items in the collection. Some iterables may also support that method.

# In[13]:


print(len('python'), len([1, 2, 3]), len({10, 20, 30}), len({'a': 1, 'b': 2}))


# Sequences (and even some iterables) may support `max` and `min` as long as the data types in the collection can be **ordered** in some sense (`<` or `>`).

# In[14]:


a = [100, 300, 200]
min(a), max(a)


# In[15]:


s = 'python'
min(s), max(s)


# In[16]:


s = {'p', 'y', 't', 'h', 'o', 'n'}
min(s), max(s)


# But if the elements do not have an ordering defined:

# In[17]:


a = [1 + 1j, 2 + 2j, 3 + 3j]
#  min(a)


# `min` and `max` will work for heterogeneous types as long as the elements are pairwise comparable (`<` or `>` is defined).
#
# For example:

# In[18]:


from decimal import Decimal


# In[19]:


t = 10, 20.5, Decimal('30.5')


# In[20]:


print(min(t), max(t))


# In[21]:


t = ['a', 10, 1000]
# min(t)


# Even `range` objects support `min` and `max`:

# In[22]:


r = range(10, 200)
print(min(r), max(r))


# #### Concatenation

# We can **concatenate** sequences using the `+` operator:

# In[23]:


[1, 2, 3] + [4, 5, 6]


# In[24]:


print((1, 2, 3) + (4, 5, 6))


# Note that the type of the concatenated result is the same as the type of the sequences being concatenated, so concatenating sequences of varying types will not work:

# In[25]:


# (1, 2, 3) + [4, 5, 6] FAILS when uncommented


# In[26]:


# 'abc' + ['d', 'e', 'f']   FAILS when uncommented


# Note: if you really want to concatenate varying types you'll have to transform them to a common type first:

# In[27]:


print((1, 2, 3) + tuple([4, 5, 6]))


# In[28]:


print(tuple('abc') + ('d', 'e', 'f'))


# In[29]:


print(''.join(tuple('abc') + ('d', 'e', 'f')))


# #### Repetition

# Most sequence types also support **repetition**, which is essentially concatenating the same sequence an integer number of times:

# In[30]:


print('abc' * 5)


# In[31]:


print([1, 2, 3] * 5)


# We'll come back to some caveats of concatenation and repetition in a bit.

# #### Finding things in Sequences

# We can find the index of the occurrence of an element in a sequence:

# In[32]:


s = "gnu's not unix"


# In[33]:


print(s.index('n'))


# In[34]:


print(s.index('n', 1), s.index('n', 2), s.index('n', 8))


# An exception is raised of the element is not found, so you'll want to catch it if you don't want your app to crash:

# In[35]:


print(s.index('n', 13))


# In[36]:


try:
    idx = s.index('n', 13)
except ValueError:
    print('not found')


# Note that these methods of finding objects in sequences do not assume that the objects in the sequence are ordered in any way. These are basically searches that iterate over the sequence until they find (or not) the requested element.
#
# If you have a sorted sequence, then other search techniques are available - such as binary searches. I'll cover some of these topics in the extras section of this course.

# #### Slicing

# We'll come back to slicing in a later lecture, but sequence types generally support slicing, even ranges (as of Python 3.2). Just like concatenation, slices will return the same type as the sequence being sliced:

# In[37]:


s = 'python'
l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# In[38]:


print(s[0:3], s[4:6])


# In[39]:


print(l[0:3], l[4:6])


# It's ok to extend ranges past the bounds of the sequence:

# In[40]:


s[4:1000]


# If your first argument in the slice is `0`, you can even omit it. Omitting the second argument means it will include all the remaining elements:

# In[41]:


print(s[0:3], s[:3])


# In[42]:


print(s[3:1000], s[3:], s[:])


# We can even have extended slicing, which provides a start, stop and a step:

# In[43]:


print(s, s[0:5], s[0:5:2])


# In[44]:


print(s, s[::2])


# Technically we can also use negative values in slices, including extended slices (more on that later):

# In[45]:


print(s, s[-3:-1], s[::-1])


# In[46]:


r = range(11)  # numbers from 0 to 10 (inclusive)


# In[47]:


print(r)
print(list(r))


# In[48]:


print(r[:5])


# In[49]:


print(list(r[:5]))


# As you can see, slicing a range returns a range object as well, as expected.

# #### Hashing

# Immutable sequences generally support a `hash` method that we'll discuss in detail in the section on mapping types:

# In[50]:


l = (1, 2, 3)
print(hash(l))


# In[51]:


s = '123'
print(hash(s))


# In[52]:


r = range(10)
print(hash(r))


# But mutable sequences (and mutable types in general) do not:

# In[53]:


l = [1, 2, 3]


# In[54]:


print(hash(l))


# Note also that a hashable sequence, is no longer hashable if one (or more) of it's elements are not hashable:

# In[55]:


t = (1, 2, [10, 20])
print(hash(t))


# But this would work:

# In[56]:


t = ('python', (1, 2, 3))
print(hash(t))


# In general, immutable types are likely hashable, while immutable types are not. So numbers, strings, tuples, etc are hashable, but lists and sets are not:

# In[57]:


from decimal import Decimal
d = Decimal(10.5)
print(hash(d))


# Sets are not hashable:

# In[58]:


s = {1, 2, 3}
print(hash(s))


# But frozensets, an immutable variant of the set, are:

# In[59]:


s = frozenset({1, 2, 3})


# In[60]:


print(hash(s))


# #### Caveats with Concatenation and Repetition

# Consider this:

# In[61]:


x = [2000]


# In[62]:


print(id(x[0]))


# In[63]:


l = x + x


# In[64]:


print(l)


# In[65]:


print(id(l[0]), id(l[1]))


# As expected, the objects in `l[0]` and `l[1]` are the same.
#
# Could also use:

# In[66]:


print(l[0] is l[1])


# This is not a big deal if the objects being concatenated are immutable. But if they are mutable:

# In[67]:


x = [[0, 0]]
print(l = x + x)


# In[68]:


l


# In[69]:


print(l[0] is l[1])


# And then we have the following:

# In[70]:


l[0][0] = 100


# In[71]:


print(l[0])


# In[72]:


print(l)


# Notice how changing the 1st item of the 1st element also changed the 1st item of the second element.

# While this seems fairly obvious when concatenating using the `+` operator as we have just done, the same actually happens with repetition and may not seem so obvious:

# In[73]:


x = [[0, 0]]


# In[74]:


m = x * 3


# In[75]:


print(m)


# In[76]:


m[0][0] = 100


# In[77]:


print(m)


# And in fact, even `x` changed:

# In[78]:


print(x)


# If you really want these repeated objects to be different objects, you'll have to copy them somehow. A simple list comprehensions would work well here:

# In[79]:


x = [[0, 0]]
m = [e.copy() for e in x * 3]


# In[80]:


print(m)


# In[81]:


m[0][0] = 100


# In[82]:


print(m)


# In[83]:


print(x)

