#!/usr/bin/env python
# coding: utf-8

# ### The For Loop

# In Python, an **iterable** is an **object** capable of returning values one at a time.
# 
# Many objects in Python are iterable: lists, strings, file objects and many more.

# Note: Our definition of an iterable did not state it was a collection of values - we only said it is an object that can return values one at a time - that's a subtle difference that we'll examine when we look into iterators and generators.

# The **for** keyword can be used to iterate an iterable.

# If you come with a background in another programming language, you have probably seen **for** loops defined this way:
# 
# ``for (int i=0; i < 5; i++) {
#     //code block
# }``

# This form of the **for** loop is simply a _repetition_, very similar to a **while** loop - in fact it is equivalent to what we could write in Python as follows:

# In[4]:


i = 0
while i < 5:
    #code block
    print(i)
    i += 1
i = None


# But that's **NOT** what the **for** statement does in Python - the **for** statement is a way to **iterate** over iterables, and has nothing to do with the **for** loop we just saw. The closest equivalent we have in Python is the **while** loop written as above.

# To use the **for** loop in Python, we **require** an iterable object to work with.

# A simple iterable object is generated via the ``range()`` function

# In[3]:


for i in range(5):
    print(i)


# Many objects are iterable in Python:

# In[5]:


for x in [1, 2, 3]:
    print(x)


# In[6]:


for x in 'hello':
    print(x)


# In[7]:


for x in ('a', 'b', 'c'):
    print(x)


# When we iterate over an iterable, each iteration returns the "next" value (or object) in the iterable:

# In[8]:


for x in [(1, 2), (3, 4), (5, 6)]:
    print(x)


# We can even assign the individual tuple values to specific named variables:

# In[9]:


for i, j in [(1, 2), (3, 4), (5, 6)]:
    print(i, j)


# We will cover iterables in a lot more detail later in this course.

# The **break** and **continue** statements work just as well in **for** loops as they do in **while** loops:

# In[10]:


for i in range(5):
    if i == 3:
        continue
    print(i)


# In[11]:


for i in range(5):
    if i == 3:
        break
    print(i)


# The **for** loop, like the **while** loop, also supports an **else** clause which is executed if and only if the loop terminates normally (i.e. did not exit because of a **break** statement)

# In[17]:


for i in range(1, 5):
    print(i)
    if i % 7 == 0:
        print('multiple of 7 found')
        break
else:
    print('No multiples of 7 encountered')


# In[18]:


for i in range(1, 8):
    print(i)
    if i % 7 == 0:
        print('multiple of 7 found')
        break
else:
    print('No multiples of 7 encountered')


# Similarly to the **while** loop, **break** and **continue** work just the same in the context of a **try** statement's **finally** clause.

# In[14]:


for i in range(5):
    print('--------------------')
    try:
        10 / (i - 3)
    except ZeroDivisionError:
        print('divided by 0')
        continue
    finally:
        print('always runs')
    print(i)


# There are a number of standard techniques to iterate over iterables:

# In[24]:


s = 'hello'
for c in s:
    print(c)


# But sometimes, for indexable iterable types (e.g. sequences), we want to also know the index of the item in the loop:

# In[23]:


s = 'hello'
i = 0
for c in s:
    print(i, c)
    i += 1


# Slightly better approach might be:

# In[27]:


s = 'hello'

for i in range(len(s)):
    print(i, s[i])


# or even better:

# In[28]:


s = 'hello'

for i, c in enumerate(s):
    print(i, c)


# We'll come back to all these iteration techniques in a lot more detail throughout this course.
