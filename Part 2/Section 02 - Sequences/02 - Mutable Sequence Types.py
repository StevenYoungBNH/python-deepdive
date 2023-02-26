#!/usr/bin/env python
# coding: utf-8

# ### Mutable Sequences

# When dealing with mutable sequences, we have a few more things we can do - essentially adding, removing and replacing elements in the sequence.
# 
# This **mutates** the sequence. The sequence's memory address has not changed, but the internal **state** of the sequence has.

# #### Replacing Elements

# We can replace a single element as follows:

# In[1]:


l = [1, 2, 3, 4, 5]
print(id(l))
l[0] = 'a'
print(id(l), l)


# We can remove all elements from the sequence:

# In[2]:


l = [1, 2, 3, 4, 5]
l.clear()
print(l)


# Note that this is **NOT** the same as doing this:

# In[3]:


l = [1, 2, 3, 4, 5]
l = []
print(l)


# The net effect may look the same, `l` is an empty list, but observe the memory addresses:

# In[4]:


l = [1, 2, 3, 4, 5]
print(id(l))
l.clear()
print(l, id(l))


# vs

# In[5]:


l = [1, 2, 3, 4, 5]
print(id(l))
l = []
print(l, id(l))


# In the second case you can see that the object referenced by `l` has changed, but not in the first case.

# Why might this be important?

# Suppose you have the following setup:

# In[6]:


suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
alias = suits
suits = []
print(suits, alias)


# But using clear:

# In[7]:


suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
alias = suits
suits.clear()
print(suits, alias)


# Big difference!!

# We can also replace elements using slicing and extended slicing. Here's an example, but we'll come back to this in a lot of detail:

# In[8]:


l = [1, 2, 3, 4, 5]
print(id(l))
l[0:2] = ['a', 'b', 'c', 'd', 'e']
print(id(l), l)


# #### Appending and Extending

# We can also append elements to the sequence (note that this is **not** the same as concatenation):

# In[9]:


l = [1, 2, 3]
print(id(l))
l.append(4)
print(l, id(l))


# If we had "appended" the value `4` using concatenation:

# In[10]:


l = [1, 2, 3]
print(id(l))
l = l + [4]
print(id(l), l)


# If we want to add more than one element at a time, we can extend a sequence with the contents of any iterable (not just sequences):

# In[11]:


l = [1, 2, 3, 4, 5]
print(id(l))
l.extend({'a', 'b', 'c'})
print(id(l), l)


# Of course, since we extended using a set, there was not gurantee of positional ordering.

# If we extend with another sequence, then positional ordering is retained:

# In[12]:


l = [1, 2, 3]
l.extend(('a', 'b', 'c'))
print(l)


# #### Removing Elements

# We can remove (and retrieve at the same time) an element from a mutable sequence:

# In[13]:


l = [1, 2, 3, 4]
print(id(l))
popped = l.pop(1)
print(id(l), popped, l)


# If we do not specify an index for `pop`, then the **last** element is popped:

# In[14]:


l = [1, 2, 3, 4]
popped = l.pop()
print(popped)
print(id(l), popped, l)


# #### Inserting Elements

# We can insert an element at a specific index. What this means is that the element we are inserting will be **at** that index position, and element that was at that position and all the remaining elements to the right are pushed out:

# In[15]:


l = [1, 2, 3, 4]
print(id(l))
l.insert(1, 'a')
print(id(l), l)


# #### Reversing a Sequence

# We can also do in-place reversal:

# In[16]:


l = [1, 2, 3, 4]
print(id(l))
l.reverse()
print(id(l), l)


# We can also reverse a sequence using extended slicing (we'll come back to this later):

# In[17]:


l = [1, 2, 3, 4]
l[::-1]


# But this is **NOT** mutating the sequence - the slice is returning a **new** sequence - that happens to be reversed.

# In[18]:


l = [1, 2, 3, 4]
print(id(l))
l = l[::-1]
print(id(l), l)


# #### Copying Sequences

# We can create a copy of a sequence:

# In[19]:


l = [1, 2, 3, 4]
print(id(l))
l2 = l.copy()
print(id(l2), l2)


# Note that the `id` of `l` and `l2` is not the same.

# In this case, using slicing does work the same as using the `copy` method:

# In[20]:


l = [1, 2, 3, 4]
print(id(l))
l2 = l[:]
print(id(l2), l2)


# As you can see in both cases we end up with new objects.
# 
# So, use copy() or [:] - up to you, they end up doing the same thing.

# We'll come back to copying in some detail in an upcoming video as this is an important topic with some subtleties.
