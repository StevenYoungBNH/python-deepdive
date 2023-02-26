#!/usr/bin/env python
# coding: utf-8

# ### Serpy

# If you're just looking for deserialization, then `Serpy` might work for you. It is extremely fast, but only provides serialization.
# 
# You can read more about Serpy here: https://serpy.readthedocs.io/en/latest/
# 
# Here's a simple example first, using our goto Person object.

# In[1]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'


# In[2]:


import serpy


# Very similarly to `Marshmallow` we need to define a schema for the serialization - Serpy calls those objects serializers:

# In[3]:


class PersonSerializer(serpy.Serializer):
    name = serpy.StrField()
    age = serpy.IntField()


# In[4]:


p1 = Person('Michael Palin', 75)


# In[5]:


PersonSerializer(p1).data


# Of course, we can get more complex schemas defined.
# 
# Let's implement a schema for our `Movie` example we did in a previous video on Marshmallow.

# In[6]:


class Movie:
    def __init__(self, title, year, actors):
        self.title = title
        self.year = year
        self.actors = actors


# In[7]:


class MovieSerializer(serpy.Serializer):
    title = serpy.StrField()
    year = serpy.IntField()
    actors = PersonSerializer(many=True)


# In[8]:


p2 = Person('John Cleese', 79)


# In[9]:


movie = Movie('Parrot Sketch', 1989, [p1, p2])


# In[10]:


movie.title, movie.year, movie.actors


# In[11]:


MovieSerializer(movie).data


# Note that the result of serialization is to a basic Python dictionary, and you can takes this further to JSON or YAML using the standard library `json` module or `PyYaml`.
# 
# For example:

# In[12]:


import json
import yaml


# In[13]:


json.dumps(MovieSerializer(movie).data)


# In[14]:


print(yaml.dump(MovieSerializer(movie).data, 
          default_flow_style=False))

