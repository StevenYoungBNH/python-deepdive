#!/usr/bin/env python
# coding: utf-8

# ### Set Operations

# Let's go over the set operations that are available in Python.

# ##### Intersections

# There's two ways to calculate the intersection of sets:

# In[1]:


s1 = {1, 2, 3}
s2 = {2, 3, 4}


# In[2]:


s1.intersection(s2)


# In[4]:


s1 & s2


# We can computer the intersection of more than just two sets at a time:

# In[6]:


s1 = {1, 2, 3}
s2 = {2, 3, 4}
s3 = {3, 4, 5}


# In[7]:


s1.intersection(s2, s3)


# In[8]:


s1 & s2 & s3


# ##### Unions

# There's also two ways to calculate the union of two sets:

# In[9]:


s1 = {1, 2, 3}
s2 = {3, 4, 5}


# In[10]:


s1.union(s2)


# In[11]:


s1 | s2


# We can compute the union of more than two sets:

# In[12]:


s3 = {5, 6, 7}


# In[13]:


s1.union(s2, s3)


# In[14]:


s1 | s2 | s3


# ##### Disjointedness

# Two sets are disjoint if their intersection is empty:

# In[15]:


s1 = {1, 2, 3}
s2 = {2, 3, 4}
s3 = {30, 40, 50}


# In[16]:


print(s1.isdisjoint(s2))
print(s2.isdisjoint(s3))


# Of course we could use the cardinality of the intersection instead:

# In[17]:


len(s1 & s2)


# In[18]:


len(s2 & s3)


# Or, since empty sets are falsy:

# In[19]:


bool(set())


# In[20]:


bool({0})


# we can also use the associated truth value:

# In[21]:


if {1, 2} & {2, 3}:
    print('sets are not disjoint')


# In[22]:


if not {1, 2} & {3, 4}:
    print('sets are disjoint')


# ##### Differences

# The difference of two sets can also be computed in two different ways:

# In[23]:


s1 = {1, 2, 3, 4, 5}
s2 = {4, 5}


# In[24]:


s1 - s2


# In[25]:


s1.difference(s2)


# Of course, with the method we can use iterables as well:

# In[26]:


s1.difference([4, 5])


# Note that the difference operator is not commutative, i.e. it does not hold in general that
# ```
# s1 - s2 = s2 - s1
# ```

# In[27]:


s2 - s1


# ##### Symmetric Difference

# We can calculate the symmetirc difference of two sets also in two ways:

# In[28]:


s1 = {1, 2, 3, 4, 5}
s2 = {4, 5, 6, 7, 8}


# In[29]:


s1.symmetric_difference(s2)


# In[ ]:


s1 ^ s2


# In[31]:


s2^s1  #symmetric difference is communtative s young 10/17/2022


# Remember that the symmetric difference of two sets results in the difference of the union and the intersection of the two sets:

# In[32]:


(s1 | s2) - (s1 & s2)


# ##### Subsets and Supersets

# With containmnent we have the notion of proper containment (i.e strictly contained, not equal) and just containment (contained, possibly equal).
# This is analogous to the concept of (`i < j` and `i <= j`)

# In[40]:


s1 = {1, 2, 3}
s2 = {1, 2, 3}
s3 = {1, 2, 3, 4}
s4 = {10, 20, 30}


# In[41]:


s1.issubset(s2)


# In[42]:


s1 <= s2


# For strict containment there is no set method - we have to use the operator, or a combination of methods/operators:

# In[43]:


s1 < s2


# In[44]:


s1.issubset(s2) and s1 != s2


# In[45]:


s1 < s3


# In[46]:


s1 <= s4


# An analogous situation with supersets:

# In[47]:


s2.issuperset(s1)


# In[48]:


s2 >= s1


# In[49]:


s2 > s1


# Be careful with these set containment operators, they do not work quite the same way as with numbers for example:

# With numbers, if
# ```
# a >= b --> False - This had been a<=b  a =10, b=10 a<=b -> True but would be False for a<b
# ```
# then it follows that
# ```
# a < b --> True
# ```
# 
# This is not the case with set containment:

# In[50]:


s1 = {1, 2, 3}
s2 = {10, 20, 30}


# As you can see these two sets are non-empty and disjoint, and containment works as follows:

# In[51]:


s1 <= s2


# In[52]:


s1 > s2


# In[53]:


s1 < s2


# In[54]:


s1 >= s2


# In[55]:


s1 == s2


# There's really not a whole lot more to say about the various set operations themselves - they are quite easy.
# Where they really shine is in their application to diverse problems, especially when dealing with dictionary keys as we saw earlier.

# ##### Enhanced Set Methods

# There's a slight wrinkle to some of these operations we just saw.
# 
# When we use the operators (`&`, `|`, `-`) we have to deal with sets on both sides of the operator:

# In[56]:


{1, 2} & [2, 3]


# But when we work with the method equivalent, we do not have that restriction - in fact the argument to these methods can be an iterable in general, not just a set:

# In[57]:


{1, 2}.intersection([2, 3])


# What happens is that Python implicitly converts any iterable to a set then finds the intersection.

# However, these iterables must contain hashable elements - they need not be unique (they will eventually be made to consist of unique elements):

# In[58]:


{1, 2}.intersection([[1,2]])


# This means that when we want to find the intersection of two `lists` for example, we could proceed this way:

# In[59]:


l1 = [1, 2, 3]
l2 = [2, 3, 4]


# In[60]:


set(l1).intersection(l2)


# ##### Side Note: Why the choice of `&`, `|` , `^` for unions, intersections and symmetric differences?

# You might be wondering why Python chose those particular symbols.
# 
# Python also uses these operators for bitwise manipulation.
# 
# `&` and `|` seem like a perfectly natural fit when you consider that
# ```
# s1 & s2
# ```
# means the elements that belong to `s1` **and** `s2`, 
# 
# and
# ```
# s1 | s2
# ```
# means the elements that belong to `s1` **or** `s2`.
# 
# Let's look at the bitwise operations:

# Let's look at these two integers:

# In[61]:


a = 0b101010
b = 0b110100


# In[62]:


a, b


# And these are just two integers, we just chose to create them using a binary literal:

# In[63]:


type(a), type(b)


# Now consider that `1` means `True`, and `0` means `False`:
# * `1 and 0` or `1 & 0` --> `0`
# * `1 or 0` or `1 | 0` --> `1`
# * and so on

# Let's use the bitwise Python and (`&`) operator on those two numbers:

# In[64]:


c = a & b
print(c)


# What we really need to do is look at the representation of this result:

# In[65]:


bin(c)


# So this is the result:
# ```
# 1 0 1 0 1 0
# 1 1 0 1 0 0
# -----------
# 1 0 0 0 0 0
# ```

# As you can see we performed a bitwise `and` between the two values. Very similar to asking whether `1` is in the intersection of corresponding slots.
# 
# The same happens with `|`, the bitwise `or` operator and unions:

# In[66]:


c = a | b


# In[67]:


bin(c)


# And again, looking at the bits themselves:
# ```
# 1 0 1 0 1 0
# 1 1 0 1 0 0
# -----------
# 1 1 1 1 1 0
# ```
# 
# this is like asking whether `1` is in the union of corresponding slots

# Now for the symmetric difference.
# There is another boolean algebra operation called `xor`, denoted by `^`.
# This one works this way:
# ```
# x xor y --> True if x is True or y is True, but not both
# ```
# 

# In[68]:


print(bin(a))
print(bin(b))
print(bin(a^b))


# Let's see the bits again:
# ```
# 1 0 1 0 1 0
# 1 1 0 1 0 0
# -----------
# 0 1 1 1 1 1
# ```
# 
# If we make two corresponding slots into sets and find the symmetric difference between the two, what do we get?

# In[69]:


{1} ^ {1}


# In[70]:


{0} ^ {1}


# In[71]:


{0} ^ {0}


# So we can ask if `1` is in `{0} ^ {1}` - which is exactly what the bitwise `xor` (`^`) operator evaluates to in the above example.
