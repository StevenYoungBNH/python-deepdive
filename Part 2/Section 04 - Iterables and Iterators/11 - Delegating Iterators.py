#!/usr/bin/env python
# coding: utf-8

# ### Delegating Iterators

# Often we write classes that use some existing iterable for the data contained in our class. By default, that class is not iterable, and we would need to implement an iterator for our class and implement the `__iter__` method in our class to return new instances of that iterator.

# But, if our underlying data structure for our class is already an iterable, there's a much quicker way of doing it - delegation.

# We'll start with a really simple example first:

# In[3]:


from collections import namedtuple

Person = namedtuple('Person', 'first last')


# In[4]:


class PersonNames:
    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize()
                             + ' ' + person.last.capitalize()
                            for person in persons]
        except (TypeError, AttributeError):
            self._persons = []


# In[5]:


persons = [Person('michaeL', 'paLin'), Person('eric', 'idLe'), 
           Person('john', 'cLeese')]


# In[13]:


person_names = PersonNames(persons)


# Technically we can see the underlying data by accessing the (pseudo) private variable `_persons`.

# In[14]:


person_names._persons


# But we really would prefer making our `PersonNames` instances iterable.
# 
# To do so we need to implement the `__iter__` method that returns an iterator that can be used for iterating over the `_persons` list.
# 
# But lists are iterables, so they can provide an iterator, and that's precisely what we'll do - we'll **delegate** our own iterator, to the list's iterator:

# In[8]:


class PersonNames:
    def __init__(self, persons):
        try:
            self._persons = [person.first.capitalize()
                             + ' ' + person.last.capitalize()
                            for person in persons]
        except TypeError:
            self._persons = []
    
    def __iter__(self):
        return iter(self._persons)


# And now, `PersonNames` is iterable!

# In[15]:


persons = [Person('michaeL', 'paLin'), Person('eric', 'idLe'), 
           Person('john', 'cLeese')]
person_names = PersonNames(persons)


# In[16]:


for p in person_names:
    print(p)


# And of course we can sort, use list comprehensions, and so on - our PersonNames **is** an iterable.

# Here we sort the names based on the full name, then split the names (on the space) and return a tuple of first name, last name:

# In[20]:


[tuple(person_name.split()) for person_name in sorted(person_names)]


# Or, if we want to sort based on the last name:

# In[21]:


sorted(person_names, key=lambda x: x.split()[1])

