#!/usr/bin/env python
# coding: utf-8

# ### Creating Sets

# Just like dictionaries, there is a variety of ways to create sets.
# 
# First we have set literals:

# In[1]:


s = {'a', 100, (1,2)}


# In[2]:


type(s)


# To create an empty set we cannot use `{}` since that would create an empty dictionary:

# In[3]:


d = {}
type(d)


# Instead, we have to use the `set()` function:

# In[4]:


s = set()


# In[5]:


type(s)


# This brings up the second way we can create sets. We can use the `set()` function and pass it an iterable:

# In[6]:


s = set([1, 2, 3])


# In[7]:


s


# or even:

# In[8]:


s = set(range(10))


# In[9]:


s


# Of course we are restricted to an iterable of hashable elements only.
# 
# So this would not work:

# In[10]:


s = set([[1,2], [3,4]])


# What might surprise you is this:

# In[11]:


d = {'a': 1, 'b': 2}
s = set(d)


# See? No exception!
# 
# But consider what happens when we iterate a dictionary:

# In[12]:


for e in d:
    print(e)


# We just get the keys back! All dictionary keys are hashable, and therefore we can always create a set from a dictionary, but it will just contain the keys:

# In[13]:


s


# Next we can use a **set comprehension** to create a set. It looks and works almost the same as a dictionary comprehension - but a set, unlike a dictionary, has no associated values. 
# Here's an example:

# In[14]:


s = {c for c in 'python'}


# In[15]:


s


# Of course, we do not really need to use a comprehension here. Since strings are iterables of characters (which are hashable), we can create a set from the characters in a string as follows:

# In[16]:


s = set('python')
s


# Just like we have iterable unpacking and dictionary unpacking, we also have set unpacking:

# In[17]:


s1 = {'a', 'b', 'c'}
s2 = {10, 20, 30}


# To combine both elements of these sets, we cannot do this:

# In[18]:


s = {s1, s2}


# This would be a set of sets - and sets are not hashable anyway (we could use a frozenset, but more about those later).
# 
# What we want is to unpack the elements of the sets into something else.
# 
# We could create a set containing all these elements:

# In[19]:


s = {*s1, *s2}


# In[20]:


s


# What's interesting about the unpacking though, is that we are not restricted to just creating another set:

# In[21]:


l = [*s1, *s2]


# In[22]:


l


# or even to pass as arguments to a function - with a big caveat!

# In[23]:


def my_func(a, b, c):
    print(a, b, c)


# In[24]:


args = {20, 10, 30}


# We cannot just pass the set directly to `my_func` because it expects three arguments, but we can unpack the set before we pass it:

# In[25]:


my_func(*args)


# Notice the order of the arguments! As we know, order of elements in a set is considered random (it's not of course, but for all practical purposes it might as well be).
# 
# In some cases however, it might not matter.
# Consider this function:

# In[26]:


def averager(*args):
    total = 0
    for arg in args:
        total += arg
    return total / len(args)


# In[27]:


averager(10, 20, 30)


# #### Distinct Elements

# We know that set elements must be distinct - so how do all these methods we have seen for creating sets behave when we have repeated elements?
# 
# Let's take a look at each, one at a time:

# In[28]:


s = {'a', 'b', 'c', 'a', 'b', 'c'}
s


# As you can see, Python just discards any repeated element.
# 
# The same happens with the `set()` function:

# In[29]:


s = set('baabaa')
s


# And the same with a comprehension:

# In[30]:


s = {c for c in 'moomoo'}
s


# Now unpacking is a little different. If we unpack into a set, then sure, elements will remain distinct:

# In[31]:


s1 = {10, 20, 30}
s2 = {20, 30, 40}
s = {*s1, *s2}
s


# But if we unpack into a tuple for example:

# In[32]:


t = (*s1, *s2)


# In[33]:


t


# As you can see, we get repeated elements.

# #### Application

# So, one really interesting application of sets and the fact that their elements are unique, is finding unique elements from collections whose elements might not be.
# 
# Consider this problem. We have a string, and we want to assign a score to the string based on how many distinct characters of the alphabet it uses.
# 
# (I'm considering an alphabet here to be 'a' - 'z'). So the total length of that alphabet is 26, and we can score a string this way:

# In[34]:


s = 'abcdefghijklmnopqrstuvwxyz'
distinct = set(s)
score = len(s) / 26
score


# Let's write a function to do this, (and remove any characters that are not part of our 'alphabet'):

# In[35]:


def scorer(s):
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    s = s.lower()
    distinct = set(s)
    # we want to only count characters that are in our alphabet
    effective = distinct & alphabet
    return len(effective) / len(alphabet)


# In[36]:


scorer(s)


# In[37]:


scorer('baa baa')


# In[38]:


2 / 26


# In[39]:


scorer('baa baa baa!!! 123')


# In[40]:


scorer('the quick brown fox jumps over the lazy dog')


# Often we are presented with problems where we have a list, or other collection, and we just want to find the unique elements of that list.
# As long as the elements are all hashable, we can easily do this using sets!
