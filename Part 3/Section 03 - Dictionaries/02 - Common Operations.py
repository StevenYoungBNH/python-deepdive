#!/usr/bin/env python
# coding: utf-8

# ### Common Operations

# You should already be aware of many of these, so I'll only spend time on some of the more interesting ones.

# Dictionaries support the `len` function - this simply returns the number of key/value pairs in the dictionary:

# In[1]:


d = dict(zip('abc', range(1, 4)))
d


# In[2]:


len(d)


# We can retrieve an element from a dictionary using `[]` notation, providing the key. If the key is not present we will get a `KeyError` exception:

# In[3]:


d['a']


# In[4]:


d['python']


# Sometimes though, we do not want an exception to happen, and we want to provide some 'default' value instead.
# We could certainly catch the exception, but that's clunky. Instead we can use the `get` instance method:

# In[5]:


d.get('a')


# In[6]:


result = d.get('python')
print(result)


# As you can see, we do not get an exception, we simply get `None` back. We can actually specify the default to use when the key is not found:

# In[7]:


d.get('python', 0)


# This can be quite useful when we are using a dictionary to keep track of some count for different keys that are not know ahead of time (if they were, we could use `fromkeys` to initialize a dictionary with all the keys  and initial values of `0`.

# Let's see a simple example of this:

# ##### Example

# Here we have a string where we want to count the number of each character that appears in the string.
# Since we know the alphabet is a-z, we could create a dictionary with these initial keys - but maybe the string contains characters outside of that, maybe punctuation marks, emojis, etc. So it's not really feasible to take that approach.

# In[8]:


text = 'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit amet consectetur adipisci[ng] velit, sed quia non-numquam [do] eius modi tempora inci[di]dunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur?'
counts = dict()
for c in text:
    counts[c] = counts.get(c, 0) + 1
print(counts)


# We can refine this a bit - first we'll ignore spaces, then we'll want to consider lowercase and uppercase characters as the same:

# In[9]:


counts = dict()
for c in text:
    key = c.lower().strip()
    if key:
        counts[key] = counts.get(key, 0) + 1
print(counts)


# #### Membership Tests

# We can use the `in` and `not in` operators to test the presence of a **key** in a dictionary:

# In[10]:


d = dict(a=1, b=2, c=3)


# In[11]:


'a' in d


# In[12]:


'z' in d


# In[13]:


'z' not in d


# #### Removing elements from a dictionary

# We can use the `del` operator to remove a key from a dictionary:

# In[14]:


d = dict.fromkeys('abcd', 0)


# In[15]:


d


# We can remove a key this way:

# In[16]:


del d['a']


# In[17]:


d


# If the key is not present, we will get a `KeyError` exception:

# In[18]:


del d['z']


# Just like setting elements, we may not want an exception to be raised - in which case we can use the `pop` and `popitem` instance methods instead.

# Let's start with the `pop` method first.
# We simply specify the **key** we want to remove from the dictionary. The `pop` method will not only remove the item (if the key is present), but also return the associated value:

# In[19]:


d


# In[20]:


result = d.pop('b')
result


# In[21]:


d


# In[22]:


result = d.pop('z')


# So we still get a `KeyError` exception!
# To do this, we need to specify a **default** value to use if the key is not found:

# In[23]:


result = d.pop('z', 'Not found!')
result


# The `popitem` method is similar, but slightly different. It does not take a key, it simply removes an element from the dictionary unless the dictionary is empty, in which case it will result in a `KeyError`. The method returns a **tuple** containing the key and the value that was just removed.

# Let's take a look at a simple example:

# In[24]:


d = {'a': 10, 'b': 20, 'c': 30}


# In[25]:


d.popitem()


# In[26]:


d.popitem()


# In[27]:


d.popitem()


# In[28]:


d.popitem()


# So one important thing to note here is the order in which the elements of the dictionary are popped - they are popped in reverse order from how they were inserted. So as you can see above, `c` was inserted last, and hence was popped first.
# So this is called a **LIFO** (last in, first out) order, and since dicts are ordered in Python 3.6+, this LIFO order when popping is also guaranteed.
# 
# **Versions prior to 3.6 do not guarantee this order.**

# #### Inserting keys with a default

# Sometimes we may want to insert an element in a dictionary with a default value, but only if the element is not already present:

# In[29]:


d = {'a': 1, 'b': 2, 'c': 3}


# We could do it this way:

# In[30]:


if 'z' not in d:
    d['z'] = 0


# In[31]:


d


# We could write a simple utility function to do this for us, and return the value of the item as well while we're at it:

# In[32]:


def insert_if_not_present(d, key, value):
    if key not in d:
        d[key] = value
        return value
    else:
        return d[key]


# In[33]:


print(d)


# In[34]:


result = insert_if_not_present(d, 'a', 0)
print(result, d)


# In[35]:


result = insert_if_not_present(d, 'y', 10)
print(result, d)


# But instead, we can simply use the `setdefault` instance method, which will do the work we just did:

# In[36]:


d = {'a': 1, 'b': 2, 'c': 3}
result = d.setdefault('a', 0)
print(result)
print(d)


# In[37]:


result = d.setdefault('z', 100)
print(result)
print(d)


# This is quite a useful method.
# Let's take a look at that example we did earlier that looked at how many times each character occurred in a string:

# In[38]:


text = 'Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit amet consectetur adipisci[ng] velit, sed quia non-numquam [do] eius modi tempora inci[di]dunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur?'
counts = dict()
for c in text:
    key = c.lower().strip()
    if key:
        counts[key] = counts.get(key, 0) + 1
print(counts)


# Suppose now that we just want a dictionary to track the uppercase, lowercase, and other characters in the string (i.e. kind of grouping the data by uppercase, lowercase, other) - again ignoring spaces:

# In[39]:


import string
print(string.ascii_lowercase)
print(string.ascii_uppercase)


# Here's one approach we might take:

# In[40]:


categories = {}
for c in text:
    if c != ' ':
        if c in string.ascii_lowercase:
            key = 'lower'
        elif c in string.ascii_uppercase:
            key = 'upper'
        else:
            key = 'other'
        if key not in categories:
            categories[key] = set()  # set we'll insert the value into
        
        categories[key].add(c)
for cat in categories:
    print(f'{cat}:', ''.join(categories[cat]))


# We can simplify this a bit using `setdefault`:

# In[41]:


categories = {}
for c in text:
    if c != ' ':
        if c in string.ascii_lowercase:
            key = 'lower'
        elif c in string.ascii_uppercase:
            key = 'upper'
        else:
            key = 'other'
        categories.setdefault(key, set()).add(c)

for cat in categories:
    print(f'{cat}:', ''.join(categories[cat]))


# Just to clean things up a but more, let's create a small utility function that will return the category key:

# In[42]:


def cat_key(c):
    if c == ' ':
        return None
    elif c in string.ascii_lowercase:
        return 'lower'
    elif c in string.ascii_uppercase:
        return 'upper'
    else:
        return 'other'


# In[43]:


categories = {}
for c in text:
    key = cat_key(c)
    if key:
        categories.setdefault(key, set()).add(c)

for cat in categories:
    print(f'{cat}:', ''.join(categories[cat]))


# If you are not a fan of using `if...elif...` in the `cat_key` function we could do it this way as well:

# In[44]:


def cat_key(c):
    categories = {' ': None,
                 string.ascii_lowercase: 'lower',
                 string.ascii_uppercase: 'upper'}
    for key in categories:
        if c in key:
            return categories[key]
    else:
        return 'other'


# In[45]:


cat_key('a'), cat_key('A'), cat_key('!'), cat_key(' ')


# This approach is easier to extend without having a lot of `elif` statements, but for a few categories, I find the first implementation much clearer to read and understand.

# In[46]:


categories = {}
for c in text:
    key = cat_key(c)
    if key:
        categories.setdefault(key, set()).add(c)

for cat in categories:
    print(f'{cat}:', ''.join(categories[cat]))


# We could also do it this way, creating a categories dictionary that has all the individual characters we are interested in:

# In[47]:


from itertools import chain

def cat_key(c):
    cat_1 = {' ': None}
    cat_2 = dict.fromkeys(string.ascii_lowercase, 'lower')
    cat_3 = dict.fromkeys(string.ascii_uppercase, 'upper')
    categories = dict(chain(cat_1.items(), cat_2.items(), cat_3.items()))
    # categories = {**cat_1, **cat_2, **cat_3} - I'll explain this later
    return categories.get(c, 'other')


# In[48]:


cat_key('a'), cat_key('A'), cat_key('!'), cat_key(' ')


# In[49]:


categories = {}
for c in text:
    key = cat_key(c)
    if key:
        categories.setdefault(key, set()).add(c)
        
for cat in categories:
    print(f'{cat}:', ''.join(categories[cat]))


# #### Clearing All Items

# If we want to remove all the keys in a dictionary, we can use the `clear` method:

# In[50]:


d = {'a': 1, 'b': 2, 'c': 3}


# In[51]:


d


# In[52]:


d.clear()


# In[53]:


d


# As you can see, Python dictionaries are extremely flexible and have all sorts of useful methods we can use to manipulate them.
