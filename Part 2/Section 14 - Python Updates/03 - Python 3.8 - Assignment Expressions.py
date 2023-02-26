#!/usr/bin/env python
# coding: utf-8

# ### Python 3.8 - Assignment Expressions

# Another enhancement to the Python core language that was introduced in Python 3.8 is **assignment expressions**.

# You can see the pep for it here: [pep 572](https://peps.python.org/pep-0572/)

# Remember that an expression is simply a snippet of code that is evaluated.
# 
# The following are all examples of expressions:

# In[1]:


1 + 2


# In[2]:


[1, 2, 3] + [4, 5, 6]


# In[3]:


"  python  ".lstrip().rstrip().upper()


# And an assignment is simply when we assign an expression result to a variable:

# In[4]:


a = 1 + 2
b = [1, 2, 3] + [4, 5, 6]
c = "  python  ".lstrip().rstrip().upper()


# As you can see, we have to different steps here.
# 
# We assign the result of an expression (the right hand side) to a variable (the left hand side) using the equals (`=`) sign.

# So we have two **distinct** (totally separate) aspects here - the expression, and the assignment.

# So what are **expression assignments**?

# Expression assignments allows us to assign expressions to a variable **inside** an expression, using the `:=` operator (the so-called *walrus* operator)

# Confusing? :-)

# Let's take a look at a very simple example first:

# Starting with an expression:

# In[5]:


1 + 2


# We could assign the result of that expression to some variable:

# In[6]:


a = 1 + 2


# But, we could also write the expression and assignment this way (not the parentheses that enclose the expression):

# In[7]:


a = (1 + 2)


# With the expression assignment operator, we could actually assign the result of that expression inside the expression itself:

# In[8]:


(x := 1 + 2)


# As you can see, the expression returned a result (`3`), but it also assigned that result to the variable `x`:

# In[9]:


x


# Note that the parentheses in this case are **necessary** - simply writing this would not work:

# In[10]:


x := 1 + 2


# This is because the `:=` operator must be used inside an **expression**, so we can force it by using the parentheses.

# We could even do this:

# In[11]:


a = (x := 10 + 20)


# Then, `a`, and `x` are:

# In[12]:


a, x


# Yeah, even more confusing! But in a minute I'll show you why this can be very useful.

# Before we move on to that, let's see how this assignment expression works when we deal with mutable objects such as lists:

# In[13]:


l1 = (l2 := [1, 2] + [3, 4])


# Here, `l1` was the result of the concatenation of the two lists:

# In[14]:


l1, id(l1)


# But what about `l2`? It should be a list with the same values, but is it the same object reference as `l1`?

# In[15]:


l2, id(l2)


# And indeed, they are not only the same values, but the same object.

# Usually this is not an issue, but keep it in mind because you end up with shared references that you may not realize exist.

# So now, why is this useful?

# Often, we end up writing expressions in terms of other sub expressions, not just for clarity, but sometimes to **avoid repeating** function calls or expression evaluations.

# #### Example 1

# Suppose we have some long running function:

# In[16]:


import time
import math

def slow_function(x, y):
    time.sleep(0.5)
    return round(math.sqrt(x**2 + y**2))


# Now executing this function will take about 2 seconds to run every time it is called, even when calling it with the same values (we could of course use some LRU caching, but only if the function is **deterministic** - if the function is reading data from a web site, or a database, the result for the same arguments may not be the same and so LRU caching is not even a viable option in this case).
# 
# > A **deterministic** function is a function that for the **same** inputs, always returns the **same** result:
# >
# >  Obviously the function we have above is deterministic, but this one would not be:
# >```
# >def get_price(symbol):
# >    # query an API for latest price for symbol
# >    price = ...
# >    return price
# >``` 
# > A function that returns the current date or time, or a random number, etc are all non-deterministic functions.

# So, LRU caching is not always an option.

# Let's see an example of why we would want to assign the result of our long running function to a variable, instead of just using it directly.

# In[17]:


from time import perf_counter

start = perf_counter()
even_results = []
for i in range(10):
    if slow_function(i, i) % 2 == 0:
        even_results.append(slow_function(i, i))
end = perf_counter()
print(even_results)
print(f'Elapsed: {end - start:.1f} seconds')


# Well that was painfully slow!
# 
# But notice that we are calling the same function, with the same arguments twice - we can eliminate that!

# In[18]:


start = perf_counter()
even_results = []
for i in range(10):
    result = slow_function(i, i)
    if result % 2 == 0:
        even_results.append(result)
end = perf_counter()
print(even_results)
print(f'Elapsed: {end - start:.1f} seconds')


# So we are able to speed this code up, by using that interim `result` variable - also note how `result` is basically a throw away variable (we typically would not use such a variable outside the loop itself - exceptions happen of course).

# But notice something about that code? It's ugly looking - we are building up a list by running through a loop and adding to an initially empty list, one element at a time.

# We can do better! List comprehensions of course.

# But... we can't write that `result = slow_function(i, i)` in our list comprehension - so we would be back to the original (and slower) may of doing it:

# In[19]:


start = perf_counter()
even_results = [
    slow_function(i, i)
    for i in range(10)
    if slow_function(i, i) % 2 == 0
]
end = perf_counter()
print(even_results)
print(f'Elapsed: {end - start:.1f} seconds')


# :-(

# And this is where the assignment expression operator comes in very handy:

# In[20]:


start = perf_counter()
even_results = [
    result
    for i in range(10)
    if (result := slow_function(i, i)) % 2 == 0
]
end = perf_counter()
print(even_results)
print(f'Elapsed: {end - start:.1f} seconds')


# Notice how using the `:=` operator, we assign the result of `slow_function(i, i)` to `result` as part of the expression itself, and then re-use that computed value for the elements of the list.

# You may be asking yourself, why not write it this way:

# In[21]:


del result


# In[22]:


even_results = [
    (result := slow_function(i, i))
    for i in range(10)
    if result % 2 == 0
]


# This happens because in a list comprehension, the loop starts running, then the `if` clause (if any) is evaluated, and then the element expression is evaluated - hence why we place the assignment expression in the `if`.

# **Example 2**

# Here's another scenario where this new operator could be quite useful.

# You want to return the result of an expression but only if it satisfies some criteria.
# 
# For example, let's say we write a generator function to produce n even random integers between 1 and 10:

# In[23]:


import random

random.seed(0)
def even_random(n):
    cnt = 0
    while cnt <= n:
        cnt += 1
        number = random.randint(0, 10)
        if number % 2 == 0:
            yield number


# We can then call the generator function:

# In[24]:


list(even_random(5))


# We can make our code a little more concise without losing readability by using the `:=` operator:

# In[25]:


random.seed(0)
def even_random(n):
    cnt = 0
    while (cnt := cnt + 1) <= n:
        if (number := random.randint(0, 10)) % 2 == 0:
            yield number


# In[26]:


list(even_random(5))


# #### Example 3

# Here's another example where we are consuming some generator, until some condition is met.

# Let's write a generator function:

# In[27]:


def gen():
    while True:
        yield list(range(random.randint(0, 10)))


# And let's print out a frew values from this generator:

# In[28]:


random.seed(8)
my_gen = gen()
for _ in range(10):
    print(next(my_gen))


# You'll notice that the fourth element is a list with 2 values.
# 
# What we want to do now, is process the lists yielded by the generator, until we hit a list with two values, at which point we want to stop processing it.

# We could do it this way with a `while` loop:

# In[31]:


random.seed(8)
my_gen = gen()
while True:
    l = next(my_gen)
    if len(l) <= 2:
        break
    print(l)


# Instead, we could re-write this way using the `:=` operator:

# In[32]:


random.seed(8)
my_gen = gen()
while len(l := next(my_gen)) > 2:
    print(l)


# In[ ]:




