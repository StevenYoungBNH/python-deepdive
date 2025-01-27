#!/usr/bin/env python
# coding: utf-8

# ### Assignments in Mutable Sequences

# We have seen how to mutate mutable sequences using append, insert, extend and in-place concatenation (`+=`).

# But mutable sequences also allow us to mutate the sequence by assigning values (iterables) to slices. Depending on how we specify the slice, and what the value is, we can actually insert, modify and delete elements of the sequence.

# #### Standard Slices

# ##### Replacement

# We can replace a slice of a sequence with any other iterable. They need not even be of the same length.

# In[35]:


l = [1, 2, 3, 4, 5]
id(l)


# In[36]:


l[0:3]


# In[37]:


l[0:3] = ['a', 'b', 'c', 'd']


# In[38]:


l, id(l)


# In fact, since strings are iterables, this would work too:

# In[39]:


l = [1, 2, 3, 4, 5]


# In[40]:


l[0:3] = 'python'


# In[41]:


l


# ##### Deleting

# Delete is really just a special case of replacement, where we replace with an empty iterable.

# In[27]:


l = [1, 2, 3, 4, 5]
id(l)


# We can delete a single element by defining a slice that precisely selects that element, and replacing it with an empty iterable.

# In[28]:


l[0:1]


# In[29]:


l[0:1] = []


# In[30]:


l, id(l)


# If we want, we can delete multiple element at once using the same technique:

# In[31]:


l = [1, 2, 3, 4, 5]
id(l)


# In[32]:


l[0:2]


# In[33]:


l[0:2] = []


# In[34]:


l, id(l)


# ##### Inserting

# In[18]:


l = [1, 2, 3, 4, 5]
id(l)


# Here we have to be careful if we want to insert something.
# 
# If we replace a slice that contains elements from the sequence, we'll be replacing those elements.
# 
# So what we really want here is a way to replace an empty slice in our sequence!

# Let's say we want to insert some elements at the second position in the sequence (index 1):

# In[43]:


l = [1, 2, 3, 4, 5]
id(l)


# In[44]:


l[1:2]


# The problem is that if we assign something to that slice it will replace the element `2`, and that's not what we want.

# Instead, we have to define an empty slice at the location where we want the insert to take place, in this case at index `1`:

# In[45]:


l[1:1]


# So, this is an empty slice start at `1` and ending *before* `1`

# In[46]:


l[1:1] = 'abc'


# In[47]:


l, id(l)


# And of course the memory address of `l` has not changed. We mutated the list.

# #### Side Note: Immutable Sequences

# As a side note, what would happen if we tried the same technique using immutable sequences, such as tuples for example?

# In[48]:


t = 1, 2, 3, 4, 5


# In[49]:


t[0:3] = (10, 20)


# As expected, we cannot mutate an immutable type.

# #### Extended Slices

# So now let's explore what happens if we assign iterables to extended slices.

# In[51]:


l = [1, 2, 3, 4, 5]
id(l)


# In[52]:


l[::2]


# Let's see if we can replace those items:

# In[54]:


l[::2] = ['a', 'b', 'c']


# In[55]:


l, id(l)


# Yes!! That worked, and the id of `l` is unchanged.

# There is one thing about assigning to extended slices - the length of the slice and the length of the iterable we are setting on the right hand side must have the **same length**:

# In[56]:


l = [1, 2, 3, 4, 5]


# In[57]:


l[::2]


# In[58]:


l[::2] = ['a', 'b']


# In[59]:


l[::2] = ['a', 'b', 'c', 'd']


# This means that we cannot delete items using extended slicing:

# In[60]:


l[::2] = []


# And of course insertion does not even make sense with an extended slice - remember that for insertion we need an empty slice...

# #### Note

# One last note, the right hand side can be any iterable. We saw how we could use a string for example. But any iterable, even non-sequence types will work as well.

# In[61]:


l = [1, 2, 3, 4, 5]


# In[62]:


l[3:3] = {'c', 'b', 'a'}


# In[63]:


l


# Of course, since we are inserting the values form a set, there is no guarantee of the order in which the elements will be inserted into our list.
