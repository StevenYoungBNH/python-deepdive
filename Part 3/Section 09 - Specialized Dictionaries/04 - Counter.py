#!/usr/bin/env python
# coding: utf-8

# ### Counter

# The `Counter` dictionary is one that specializes for helping with, you guessed it, counters!
# 
# Actually we used a `defaultdict` earlier to do something similar:

# In[1]:


from collections import defaultdict, Counter


# Let's say we want to count the frequency of each character in a string:

# In[2]:


sentence = 'the quick brown fox jumps over the lazy dog'


# In[3]:


counter = defaultdict(int)


# In[4]:


for c in sentence:
    counter[c] += 1


# In[5]:


counter


# We can do the same thing using a `Counter` - unlike the `defaultdict` we don't specify a default factory - it's always zero (it's a counter after all):

# In[6]:


counter = Counter()
for c in sentence:
    counter[c] += 1


# In[7]:


counter


# OK, so if that's all there was to `Counter` it would be pretty odd to have a data structure different than `OrderedDict`.
# 
# But `Counter` has a slew of additional methods which make sense in the context of counters:
# 
# 1. Iterate through all the elements of counters, but repeat the elements as many times as their frequency
# 2. Find the `n` most common (by frequency) elements
# 3. Decrement the counters based on another `Counter` (or iterable)
# 4. Increment the counters based on another `Counter` (or iterable)
# 5. Specialized constructor for additional flexibility
# 
# If you are familiar with multisets, then this is essentially a data structure that can be used for multisets.

# #### Constructor

# It is so common to create a frequency distribution of elements in an iterable, that this is supported automatically:

# In[8]:


c1 = Counter('able was I ere I saw elba')
c1


# Of course this works for iterables in general, not just strings:

# In[9]:


import random


# In[10]:


random.seed(0)


# In[11]:


my_list = [random.randint(0, 10) for _ in range(1_000)]


# In[12]:


c2 = Counter(my_list)


# In[13]:


c2


# We can also initialize a `Counter` object by passing in keyword arguments, or even a dictionary:

# In[14]:


c2 = Counter(a=1, b=10)
c2


# In[15]:


c3 = Counter({'a': 1, 'b': 10})
c3


# Technically we can store values other than integers in a `Counter` object - it's possible but of limited use since the default is still `0` irrespective of what other values are contained in the object.

# #### Finding the n most Common Elements

# Let's find the `n` most common words (by frequency) in a paragraph of text. Words are considered delimited by white space or punctuation marks such as `.`, `,`, `!`, etc - basically anything except a character or a digit.
# This is actually quite difficult to do, so we'll use a close enough approximation that will cover most cases just fine, using a regular expression:

# In[16]:


import re


# In[17]:


sentence = '''
his module implements pseudo-random number generators for various distributions.

For integers, there is uniform selection from a range. For sequences, there is uniform selection of a random element, a function to generate a random permutation of a list in-place, and a function for random sampling without replacement.

On the real line, there are functions to compute uniform, normal (Gaussian), lognormal, negative exponential, gamma, and beta distributions. For generating distributions of angles, the von Mises distribution is available.

Almost all module functions depend on the basic function random(), which generates a random float uniformly in the semi-open range [0.0, 1.0). Python uses the Mersenne Twister as the core generator. It produces 53-bit precision floats and has a period of 2**19937-1. The underlying implementation in C is both fast and threadsafe. The Mersenne Twister is one of the most extensively tested random number generators in existence. However, being completely deterministic, it is not suitable for all purposes, and is completely unsuitable for cryptographic purposes.'''


# In[18]:


words = re.split('\W', sentence)


# In[19]:


words


# But what are the frequencies of each word, and what are the 5 most frequent words?

# In[20]:


word_count = Counter(words)


# In[21]:


word_count


# In[22]:


word_count.most_common(5)


# #### Using Repeated Iteration

# In[23]:


c1 = Counter('abba')
c1


# In[24]:


for c in c1:
    print(c)


# However, we can have an iteration that repeats the counter keys as many times as the indicated frequency:

# In[25]:


for c in c1.elements():
    print(c)


# What's interesting about this functionality is that we can turn this around and use it as a way to create an iterable that has repeating elements.
# 
# Suppose we want to to iterate through a list of (integer) numbers that are each repeated as many times as the number itself.
# 
# For example 1 should repeat once, 2 should repeat twice, and so on.
# 
# This is actually not that easy to do!
# 
# Here's one possible way to do it:

# In[26]:


l = []
for i in range(1, 11):
    for _ in range(i):
        l.append(i)
print(l)


# But we could use a `Counter` object as well:

# In[27]:


c1 = Counter()
for i in range(1, 11):
    c1[i] = i


# In[28]:


c1


# In[29]:


print(c1.elements())


# So you'll notice that we have a `chain` object here. That's one big advantage to using the `Counter` object - the repeated iterable does not actually exist as list like our previous implementation - this is a lazy iterable, so this is far more memory efficient.
# 
# And we can iterate through that `chain` quite easily:

# In[30]:


for i in c1.elements():
    print(i, end=', ')


# Just for fun, how could we reproduce this functionality using a plain dictionary?

# In[31]:


class RepeatIterable:
    def __init__(self, **kwargs):
        self.d = kwargs
        
    def __setitem__(self, key, value):
        self.d[key] = value
        
    def __getitem__(self, key):
        self.d[key] = self.d.get(key, 0)
        return self.d[key]


# In[32]:


r = RepeatIterable(x=10, y=20)


# In[33]:


r.d


# In[34]:


r['a'] = 100


# In[35]:


r['a']


# In[36]:


r['b']


# In[37]:


r.d


# Now we have to implement that `elements` iterator:

# In[38]:


class RepeatIterable:
    def __init__(self, **kwargs):
        self.d = kwargs
        
    def __setitem__(self, key, value):
        self.d[key] = value
        
    def __getitem__(self, key):
        self.d[key] = self.d.get(key, 0)
        return self.d[key]
    
    def elements(self):
        for k, frequency in self.d.items():
            for i in range(frequency):
                yield k


# In[39]:


r = RepeatIterable(a=2, b=3, c=1)


# In[40]:


for e in r.elements():
    print(e, end=', ')


# #### Updating from another Iterable or Counter

# Lastly let's see how we can update a `Counter` object using another `Counter` object. 
# 
# When both objects have the same key, we have a choice - do we add the count of one to the count of the other, or do we subtract them?
# 
# We can do either, by using the `update` (additive) or `subtract` methods.

# In[41]:


c1 = Counter(a=1, b=2, c=3)
c2 = Counter(b=1, c=2, d=3)

c1.update(c2)
print(c1)


# On the other hand we can subtract instead of add counters:

# In[42]:


c1 = Counter(a=1, b=2, c=3)
c2 = Counter(b=1, c=2, d=3)

c1.subtract(c2)
print(c1)


# Notice the key `d` - since `Counters` default missing keys to `0`, when `d: 3` in `c2` was subtracted from `c1`, the counter for `d` was defaulted to `0`.

# Just as the constructor for a `Counter` can take different arguments, so too can the `update` and `subtract` methods.

# In[43]:


c1 = Counter('aabbccddee')
print(c1)
c1.update('abcdef')
print(c1)


# #### Mathematical Operations

# These `Counter` objects also support several other mathematical operations when both operands are `Counter` objects. In all these cases the result is a new `Counter` object.
# 
# * `+`: same as `update`, but returns a new `Counter` object instead of an in-place update.
# * `-`: subtracts one counter from another, but discards zero and negative values
# * `&`: keeps the **minimum** of the key values
# * `|`: keeps the **maximum** of the key values

# In[44]:


c1 = Counter('aabbcc')
c2 = Counter('abc')
c1 + c2


# In[45]:


c1 - c2


# In[46]:


c1 = Counter(a=5, b=1)
c2 = Counter(a=1, b=10)

c1 & c2


# In[47]:


c1 | c2


# The **unary** `+` can also be used to remove any non-positive count from the Counter:

# In[48]:


c1 = Counter(a=10, b=-10)
+c1


# The **unary** `-` changes the sign of each counter, and removes any non-positive result:

# In[49]:


-c1


# ##### Example

# Let's assume you are working for a company that produces different kinds of widgets.
# You are asked to identify the top 3 best selling widgets.
# 
# You have two separate data sources - one data source can give you a history of all widget orders (widget name, quantity), while another data source can give you a history of widget refunds (widget name, quantity refunded).
# 
# From these two data sources, you need to determine the top selling widgets (taking refinds into account of course).

# Let's simulate both of these lists:

# In[50]:


import random
random.seed(0)

widgets = ['battery', 'charger', 'cable', 'case', 'keyboard', 'mouse']

orders = [(random.choice(widgets), random.randint(1, 5)) for _ in range(100)]
refunds = [(random.choice(widgets), random.randint(1, 3)) for _ in range(20)]


# In[51]:


orders


# In[52]:


refunds


# Let's first load these up into counter objects.
# 
# To do this we're going to iterate through the various lists and update our counters:

# In[53]:


sold_counter = Counter()
refund_counter = Counter()

for order in orders:
    sold_counter[order[0]] += order[1]

for refund in refunds:
    refund_counter[refund[0]] += refund[1]


# In[54]:


sold_counter


# In[55]:


refund_counter


# In[56]:


net_counter = sold_counter - refund_counter


# In[57]:


net_counter


# In[58]:


net_counter.most_common(3)


# We could actually do this a little differently, not using loops to populate our initial counters.
# 
# Recall the `repeat()` function in `itertools`:

# In[59]:


from itertools import repeat


# In[60]:


list(repeat('battery', 5))


# In[61]:


orders[0]


# In[62]:


list(repeat(*orders[0]))


# So we could use the `repeat()` method to essentially repeat each widget for each item of `orders`. We need to chain this up for each element of `orders` - this will give us a single iterable that we can then use in the constructor for a `Counter` object. We can do this using a generator expression for example:

# In[63]:


from itertools import chain


# In[64]:


list(chain.from_iterable(repeat(*order) for order in orders))


# In[65]:


order_counter = Counter(chain.from_iterable(repeat(*order) for order in orders))


# In[66]:


order_counter

#### Alternate Solution not using Counter
# What if we don't want to use a `Counter` object.
# We can still do it (relatively easily) as follows:

# In[67]:


net_sales = {}
for order in orders:
    key = order[0]
    cnt = order[1]
    net_sales[key] = net_sales.get(key, 0) + cnt
    
for refund in refunds:
    key = refund[0]
    cnt = refund[1]
    net_sales[key] = net_sales.get(key, 0) - cnt

# eliminate non-positive values (to mimic what - does for Counters)
net_sales = {k: v for k, v in net_sales.items() if v > 0}

# we now have to sort the dictionary
# this means sorting the keys based on the values
sorted_net_sales = sorted(net_sales.items(), key=lambda t: t[1], reverse=True)

# Top three
sorted_net_sales[:3]

