#!/usr/bin/env python
# coding: utf-8

# ### Exercise 2 - Solution

# Suppose you have a list of all possible eye colors:

# In[1]:


eye_colors = ("amber", "blue", "brown", "gray", "green", "hazel", "red", "violet")


# Some other collection (say recovered from a database, or an external API) contains a list of `Person` objects that have an eye color property.
# 
# Your goal is to create a dictionary that contains the number of people that have the eye color as specified in `eye_colors`. The wrinkle here is that even if no one matches some eye color, say `amber`, your dictionary should still contain an entry `"amber": 0`.

# Here is some sample data:

# In[2]:


class Person:
    def __init__(self, eye_color):
        self.eye_color = eye_color


# In[3]:


from random import seed, choices
seed(0)
persons = [Person(color) for color in choices(eye_colors[2:], k = 50)]


# As you can see we built up a list of `Person` objects, none of which should have `amber` or `blue` eye colors

# Write a function that returns a dictionary with the correct counts for each eye color listed in `eye_colors`.

# We're going to use the `Counter` class for this problem.
# However, simply counting the eye colors in the `person` list is not going to be quite enough:

# In[4]:


from collections import Counter


# In[5]:


counts = Counter(p.eye_color for p in persons)


# In[6]:


counts


# As you can see we do not have entries for `amber` and `blue` for example.

# We could approach this in one of two ways:
# 1. add zero count key/value pairs after the counting has occurred
# 2. or, pre-initialize the `Counter` object with all the possible eye colors set to a count of `0`.

# Let's try the first approach:

# In[7]:


counts = Counter(p.eye_color for p in persons)


# In[8]:


result = {color: counts.get(color, 0) for color in eye_colors}


# In[9]:


result


# And now the second approach, where we initialize our Counter object with zero counts for each eye color first, and **then** do the counting:

# In[10]:


counts = Counter({color: 0 for color in eye_colors})


# In[11]:


counts


# As you can see we have each color with a count of zero - now we simply update the counter based on the results in the `persons` list:

# In[12]:


counts.update(p.eye_color for p in persons)


# In[13]:


counts


# Finally, let's package up one of those solutions into a function:

# In[14]:


def count_eye_colors(persons, possible_eye_colors):
    counts = Counter({color: 0 for color in possible_eye_colors})
    counts.update(p.eye_color for p in persons)
    return counts


# which we can then call like this:

# In[15]:


count_eye_colors(persons, eye_colors)

