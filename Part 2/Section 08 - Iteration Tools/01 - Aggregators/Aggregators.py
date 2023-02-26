#!/usr/bin/env python
# coding: utf-8

# ### Aggregators

# We have already used many built-in aggregators.

# In[1]:


def squares(n):
    for i in range(n):
        yield i**2


# In[2]:


list(squares(5))


# We can find the `min` and `max` of elements in an iterable:

# In[3]:


min(squares(5))


# In[4]:


max(squares(5))


# Be careful, all these aggregation functions will **exhaust** any iterator being used.

# In[5]:


sq = squares(5)


# In[6]:


max(sq)


# In[7]:


min(sq)


# We also have `sum`:

# In[8]:


list(squares(5))


# In[9]:


sum(squares(5))


# #### The `any` function

# The `any` function is a predicate (a function that returns `True` or `False`) that takes an iterable and returns `True` if all elements of that iterable are True (or have an associated True truth-value, i.e. **truthy**).
# 
# Remember that by default custom objects are always truthy:

# In[10]:


class Person:
    pass


# In[11]:


p = Person()


# In[12]:


bool(p)


# For numbers, anything other than `0` is truthy, and strings, lists, tuples, dictionaries, etc are falsy if they are empty.
# 
# In fact, any empty sequence type (i.e. length = 0) is falsy, including custom sequence types:

# In[13]:


class MySeq:
    def __init__(self, n):
        self.n = n
        
    def __len__(self):
        return self.n
    
    def __getitem__(self, s):
        pass


# In[14]:


my_seq = MySeq(0)


# In[15]:


bool(my_seq)


# In[16]:


my_seq = MySeq(10)


# In[17]:


bool(my_seq)


# The `any` function can be used to quickly test if any element is **truthy**:

# In[18]:


any([0, '', None])


# In[19]:


any([0, '', None, 'hello'])


# Basically, the `any` function is like doing an `or` between all the elements of the iterable, and casting the result to a Boolean:

# In[20]:


result = 0 or '' or None or 'hello'
result, bool(result)


# #### The `all` Function

# The `all` function is very similar to the `any` function, but it determines if **all** the elements of the iterable are truthy.
# 
# Basically it is equivalent to doing an `and` between all the elements of the iterable and casting the result to a Boolean.

# In[21]:


all([1, 'abc', [1, 2], range(5)])


# In[22]:


all([1, 'abc', [1, 2], range(5), ''])


# #### In Practice

# In practice, we often need to test if all elements of an iterable satisfy some criteria, not necessarily whether the elements are truthy or falsy.
# 
# But we can easily apply a predicate to an iterable to first evaluate the conditions we want, and then feed that into the `any` or `all` functions.
# 
# This is where the `map` function is extremely useful! Alternatively, we can also use generator expressions.
# 
# Let's see a few examples.

# ##### Example 1

# Suppose we want to test if an iterable contains only numeric values.

# First, we need to figure out how we determine if something is a number.
# 
# This is actually a very common question on the web, with all kinds of weird and wonderful solutions - most of which actually work (for the most part).
# 
# But the simplest is to test if the object we are looking at is an instance of the `Number` class!

# In[23]:


from numbers import Number


# In[24]:


isinstance(10, Number), isinstance(10.5, Number)


# In[25]:


isinstance(2+3j, Number)


# In[26]:


from decimal import Decimal


# In[27]:


isinstance(Decimal('10.3'), Number)


# In[28]:


isinstance(True, Number)


# On the other hand:

# In[29]:


isinstance('100', Number)


# In[30]:


isinstance([10, 20], Number)


# Now suppose we have a list (or iterable in general) and we want to see if they are all numbers:

# We could proceed with a rather clunky approach this way:

# In[31]:


l = [10, 20, 30, 40]

is_all_numbers = True
for item in l:
    if not isinstance(item, Number):
        is_all_numbers = False
        break
print(is_all_numbers)


# In[32]:


l = [10, 20, 30, 40, 'hello']

is_all_numbers = True
for item in l:
    if not isinstance(item, Number):
        is_all_numbers = False
        break
print(is_all_numbers)


# Now we can actually simplify this a little, by using the `else` clause of the `for`loop - remember that the `else` clause of a `for` loop will execute if the loop terminated normally (i.e. did not `break` out of the loop).

# In[33]:


l = [10, 20, 30, 40, 'hello']
is_all_numbers = False
for item in l:
    if not isinstance(item, Number):
        break
else: # nobreak --> all numbers
    is_all_numbers = True
print(is_all_numbers)


# Still this is clunky - there has to be a better way!
# 
# Yes, of course - the `all` function.
# 
# But we can't use it directly on the items - we're not interested in whether they are all truthy or not, we are interested in whether they are all numbers or not.
# 
# To achieve this we need to transform each element of the list using a predicate that will return `True` if the element is a number and `False` otherwise.

# We can use the `map` function to apply a function (with a single parameter) to all the elements of an iterable:

# In[34]:


map(str, [0, 1, 2, 3, 4])


# Now `map` is lazy, so let's put it into a list to see what it contains:

# In[35]:


list(map(str, [0, 1, 2, 3, 4]))


# The function we actually want to use is the `isinstance` function - but that requires **two** parameters - the element we are testing, and the `type` we are testing for.
# 
# Somehow we need to create a form of `isinstance` that only requires a single variable and simply holds the type (`Number`) fixed.
# 
# We can do this very simply using a function or a lambda.

# In[36]:


def is_number(x):
    return isinstance(x, Number)


# or, simply a lambda:

# In[37]:


lambda x: isinstance(x, Number)


# So now, let's map that function to our iterable:

# In[38]:


l


# In[39]:


list(map(lambda x: isinstance(x, Number), l))


# And of course, **now** we can use the `all` function to determine if all the elements are numbers or not:

# In[40]:


l = [10, 20, 30, 40, 'hello']
all(map(lambda x: isinstance(x, Number), l))


# In[41]:


l = [10, 20, 30, 40]
all(map(lambda x: isinstance(x, Number), l))


# A lot less typing than the first approach we did!

# If you don't like using `map` for some reason, we can easily use a generator expression as well:

# In[42]:


l = [10, 20, 30, 40]
all(isinstance(x, Number) for x in l)


# In[43]:


l = [10, 20, 30, 40, 'hello']
all(isinstance(x, Number) for x in l)


# Both approaches work equally well - use whichever one you are most comfortable with - but do try to use both and once you are comfortable with both approaches, then choose!

# ##### Example 2

# Let's look at another simple example.
# 
# Suppose we have a file and we want to make sure that all the rows in the file have length > some number.
# 
# Let's just see what data we have in our sample data file:

# In[44]:


with open('car-brands.txt') as f:
    for row in f:
        print(len(row), row, end='')


# We can easily test to make sure that every brand in our file is at least 3 characters long:

# In[45]:


with open('car-brands.txt') as f:
    result = all(map(lambda row: len(row) >= 3, f))
print(result)


# And we can test to see if any line is more than 10 characters:

# In[46]:


with open('car-brands.txt') as f:
    result = any(map(lambda row: len(row) > 10, f))
print(result)


# More than 13?

# In[47]:


with open('car-brands.txt') as f:
    result = any(map(lambda row: len(row) > 13, f))
print(result)


# Of course, we can also do this using generator expressions instead of `map`:

# In[48]:


with open('car-brands.txt') as f:
    result = any(len(row) > 13 for row in f)
print(result)

