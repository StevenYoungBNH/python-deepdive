#!/usr/bin/env python
# coding: utf-8

# ### Exercise 1 - Solution

# Let's revisit an exercise we did right after the section on dictionaries.
# 
# You have text data spread across multiple servers. Each server is able to analyze this data and return a dictionary that contains words and their frequency.
# 
# Your job is to combine this data to create a single dictionary that contains all the words and their combined frequencies from all these data sources. Bonus points if you can make your dictionary sorted by frequency (highest to lowest).
# 
# For example, you may have three servers that each return these dictionaries:

# In[1]:


d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}


# Your resulting dictionary should look like this:

# In[2]:


d = {'python': 17,
     'javascript': 15,
     'java': 13,
     'c#': 12,
     'c++': 10,
     'go': 9,
     'erlang': 5,
     'haskell': 2,
     'pascal': 1}


# If only servers 1 and 2 return data (so d1 and d2), your results would look like:

# In[3]:


d = {'python': 16,
     'javascript': 15,
     'java': 13,
     'c#': 12,
     'c++': 10, 
     'go': 9}


# This was one solution to the problem:

# In[4]:


def merge(*dicts):
    unsorted = {}
    for d in dicts:
        for k, v in d.items():
            unsorted[k] = unsorted.get(k, 0) + v
            
    # create a dictionary sorted by value
    return dict(sorted(unsorted.items(), key=lambda e: e[1], reverse=True))


# Implement two different solutions to this problem:
# 
# **a**: Using `defaultdict` objects
# 
# **b**: Using `Counter` objects

# ##### Solution a

# Using `defaultdict` objects does not greatly simplify the problem, but at least we can get rid of the `get` logic:

# In[5]:


from collections import defaultdict

def merge(*dicts):
    unsorted = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            unsorted[k] += v
            
    # create a dictionary sorted by value
    return dict(sorted(unsorted.items(), key=lambda e: e[1], reverse=True))


# In[6]:


merge(d1, d2)


# In[7]:


merge(d1, d2, d3)


# ##### Solution b

# Now that we know about the `Counter` class however, this problem is trivial:

# In[8]:


from collections import Counter

def merge(*dicts):
    unsorted = Counter()
    for d in dicts:
        unsorted.update(d)
    
    return unsorted


# In[9]:


print(merge(d1, d2))


# In[10]:


print(merge(d1, d2, d3))


# Now, the only thing still missing is the fact that even though the counters may sometimes (pure luck!) appear sorted, they are not guaranteed to be so. For example, let's add `d4` as follows:

# In[11]:


d4 = {'modula-2': 100}


# In[12]:


merge(d1, d2, d3, d4)


# As you can see, this is not sorted by frequency.
# 
# We could use the same technique we used before to sort the dictionary, but here I just want to show you an alternative.
# 
# The `Counter` objects have a method called `most_common`. We can use that method, without an argument to return all the freuqncies sorted from highest to lowest:

# In[13]:


result = merge(d1, d2, d3, d4)


# In[14]:


result.most_common()


# Only thing is we need to make this into a dictionary:

# In[15]:


dict(result.most_common())


# So, let's finalize our function:

# In[16]:


from collections import Counter

def merge(*dicts):
    result = Counter()
    for d in dicts:
        result.update(d)
    
    return dict(result.most_common())


# In[17]:


merge(d1, d2, d3, d4)

