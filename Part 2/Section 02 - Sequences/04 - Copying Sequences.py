#!/usr/bin/env python
# coding: utf-8

# ### Copying Sequences

# #### Shallow Copies

# ##### Simple Loop

# Really not a very Pythonic approach, but it works...

# In[1]:


l1 = [1, 2, 3]

l1_copy = []
for item in l1:
    l1_copy.append(item)

print(l1_copy)


# And we can see that `l1` and `l1_copy` are not the same objects:

# In[2]:


l1 is l1_copy


# ##### List Comprehension

# We can use a list comprehension to do exactly what we did in the previous example:

# In[3]:


l1 = [1, 2, 3]
l1_copy = [item for item in l1]
print(l1_copy)


# And once again, the objects are not the same:

# In[4]:


l1 is l1_copy


# ##### Using the copy() method

# Since lists are mutable sequence types, they have the `copy()` method.

# In[5]:


l1 = [1, 2, 3]
l1_copy = l1.copy()
print(l1_copy)


# And once again, the objects are different:

# In[6]:


l1 is l1_copy


# ##### Using the built-in list() Function

# The built-in `list()` function will make a list out of any iterable. This always ends up with a copy of the iterable:

# In[7]:


l1 = [1, 2, 3]


# In[8]:


l1_copy = list(l1)
print(l1_copy)


# In[9]:


l1 is l1_copy


# Note that `list()` will take in any iterable, so you can technically copy any iterable into a list:

# In[10]:


t1 = (1, 2, 3)
t1_copy = list(t1)
print(t1_copy)


# Of course, we get a list, not a tuple - so not exactly a copy.

# We've seen this before, but be careful with the `tuple()` built-in function. When we copy tuples, since they are immutable, we just get the original tuple back:

# In[11]:


t1 = (1, 2, 3)
t1_copy = tuple(t1)
print(t1_copy)


# But here, the objects are the **same**:

# In[12]:


t1 is t1_copy


# ##### Using Slicing

# We can also use slicing to copy sequences.
# 
# We'll cover slicing in detail in an upcoming lecture, but with slicing we can also access subsets of the sequence - here we use slicing to select the entire sequence:

# In[13]:


l1 = [1, 2, 3]
l1_copy = l1[:]
print(l1_copy)
print(l1 is l1_copy)


# But again, watch out with tuples!!

# In[14]:


t1 = (1, 2, 3)
t1_copy = t1[:]
print(t1_copy)
print(t1 is t1_copy)


# As you can see, since the slice was the entire tuple, a copy was not made, instead the reference to the original tuple was returned!

# Same deal with strings:

# In[15]:


s1 = 'python'
s2 = str(s1)
print(s2)
print(s1 is s2)


# In[16]:


s1 = 'python'
s2 = s1[:]
print(s2)
print(s1 is s2)


# If you're wondering why Python has that behavior, just think about it.
# 
# If you create a copy of a tuple, what are you going to do to that copy? Modify it?? You can't!
# 
# Modify the contents of a contained mutable element? Sure you can, but whether you had a copy or not, you would still be modifying the **same** element - having the sequence copied is no safer than not.
# 
# Not needed, so Python basically optimizes things for us.

# ##### The `copy` module

# In[17]:


import copy


# The `copy` module has a generic `copy` function as well:

# In[18]:


l1 = [1, 2, 3]
l1_copy = copy.copy(l1)
print(l1_copy)
print(l1 is l1_copy)


# And for tuples:

# In[19]:


t1 = (1, 2, 3)
t1_copy = copy.copy(t1)
print(t1_copy)
print(t1 is t1_copy)


# As you can see the same thing happens with tuples as we saw before.

# #### Shallow vs Deep Copies

# What we have been doing so far is creating **shallow** copies.
# 
# This means that when a sequence is copied, each element of the new sequence is bound to precisely the same memory address as the corresponding element in the original sequence:

# In[20]:


v1 = [0, 0]
v2 = [0, 0]

line1 = [v1, v2]


# In[21]:


print(line1)
print(id(line1[0]), id(line1[1]))


# Now let's make a copy of the line using any of the techniques we just looked at:

# In[22]:


line2 = line1.copy()


# In[23]:


line1 is line2


# So not the same objects. Now let's look at the contained elements themselves:

# In[24]:


print(id(line1[0]), id(line1[1]))
print(id(line2[0]), id(line2[1]))


# As you can see, the element references are the same!

# So, if we do this:

# In[25]:


line2[0][0] = 100


# In[26]:


line2


# In[27]:


line1


# `line1`'s contents has also changed.

# If we want the contained elements **also** to be copied, then we need to explicitly do so as well. This is called creating a **deep** copy.
# 
# Let's see how we might do this:

# In[28]:


v1 = [0, 0]
v2 = [0, 0]

line1 = [v1, v2]


# In[29]:


line2 = [item[:] for item in line1]


# In[30]:


print(id(line1[0]), id(line1[1]))
print(id(line2[0]), id(line2[1]))


# As you can see, now we have copies of the elements as well:

# In[31]:


line1[0][0] = 100
print(line1)
print(line2)


# and `line2` is unaffacted when we modify `line1`.
# 
# So not only did we do a copy of `line1`, but we also made a shallow copy of `v1` and `v2` as well.
# 
# But the problem is that we only went two levels deep - what if the variables `v1` and `v2` themselves contained mutable types instead of just integers? We would have to nest deeper and deeper - in general that's what a deep copy needs to do, and usually recursive approaches need to be used.

# Fortunately, Python has that functionality built-in for us so we don't have to do that!

# The `copy` module has a `deepcopy()` function we can use to create deep copies. It handles all kinds of weird situations where we might have circular references - doing it ourselves is certainly possible, but does take some work.

# In[32]:


v1 = [0, 0]
v2 = [0, 0]
line1 = [v1, v2]


# In[33]:


line2 = copy.deepcopy(line1)
print(id(line1[0]), id(line1[1]))
print(id(line2[0]), id(line2[1]))


# In[34]:


line2[0][0] = 100


# In[35]:


print(line1)
print(line2)


# And of course, it works with any level of nested objects:

# In[36]:


v1 = [11, 12]
v2 = [21, 22]
line1 = [v1, v2]

v3 = [31, 32]
v4 = [41, 42]
line2 = [v3, v4]

plane1 = [line1, line2]
print(plane1)


# In[37]:


plane2 = copy.deepcopy(plane1)


# In[38]:


print(plane2)


# In[39]:


print(plane1[0], id(plane1[0]))
print(plane2[0], id(plane2[0]))


# In[40]:


print(plane1[0][0], id(plane1[0][0]))
print(plane2[0][0], id(plane2[0][0]))


# #### Even works with custom classes

# In[41]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def __repr__(self):
        return f'Line({self.p1.__repr__()}, {self.p2.__repr__()})'


# In[42]:


p1 = Point(0, 0)
p2 = Point(10, 10)
line1 = Line(p1, p2)
line2 = copy.deepcopy(line1)

print(line1.p1, id(line1.p1))
print(line2.p1, id(line2.p1))


# As you can see, the memory address of the points are different - that was because of the deep copy.

# However, if we had done a shallow copy:

# In[43]:


p1 = Point(0, 0)
p2 = Point(10, 10)
line1 = Line(p1, p2)
line2 = copy.copy(line1)

print(line1.p1, id(line1.p1))
print(line2.p1, id(line2.p1))


# As you can see, the memory address of the points are now the **same**.
