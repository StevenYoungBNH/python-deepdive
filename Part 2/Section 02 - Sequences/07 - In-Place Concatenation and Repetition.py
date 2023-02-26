#!/usr/bin/env python
# coding: utf-8

# ### In-Place Concatenation and Repetition

# ##### In-Place Concatenation

# We saw that using concatenation ended up creating a new sequence object:

# In[1]:


l1 = [1, 2, 3, 4]
l2 = [5, 6]
print(id(l1), l1)
print(id(l2), l2)


# In[2]:


l1 = l1 + l2
print(id(l1), l1)


# But watch what happens when we use the in-place concatenation operator `+=:

# In[3]:


l1 = [1, 2, 3, 4]
l2 = [5, 6]
print(id(l1), l1)
print(id(l2), l2)


# In[4]:


l1 += l2
print(id(l1), l1)


# Notice how the `id` of `l1` has **not** changed - it is the same object, just mutated!

# So far in this course I have often said that:
# 
# `a = a + 1`
# 
# and 
# 
# `a += 1`
# 
# are the same thing.
# 
# And for immutable objects such as integers, that is indeed true.
# 
# But in fact `+` and `+=` are two different operators.

# It is interesting to note that the implementation of `+=` for lists will actually extend the list given any iterable, not just another list. This is really just the particular implementation of that operator for lists.

# In[5]:


l1 = [1, 2, 3, 4]
t1 = 5, 6, 7
print(id(l1), l1)
print(id(t1), t1)


# In[6]:


l1 += t1
print(id(l1), l1)


# And this will work with other iterables as well:

# In[7]:


l1 += range(8, 11)
print(id(l1), l1)


# or even with iterable non-sequence types:

# In[8]:


l1 += {11, 12, 13}
print(id(l1), l1)


# Of course, this will **not work** with **immutable** sequence types, such as tuples or strings:

# In[9]:


t1 = 1, 2, 3
t2 = 4, 5, 6
print(id(t1), t1)
print(id(t2), t2)


# In[10]:


print(id(t1), t1)


# We cannot mutate an immutable container!
# What happens is that `+=` is not actually defined for the `tuple`, and so Python essentially executed this code:
# 
# `t1 = t1 + t2`
# 
# which, as we already know, always creates a new object.

# ##### In-Place Repetition

# A similar result holds for in-place repetition.
# 
# Let's see this using a list (mutable sequence type) first:

# In[11]:


l = [1, 2, 3]
print(id(l), l)


# In[12]:


l *= 2
print(id(l), l)


# But obviously this operator will work differently if the sequence type is immutable:

# In[13]:


t = (1, 2, 3)
print(id(t), t)


# In[14]:


t *= 2
print(id(t), t)

