#!/usr/bin/env python
# coding: utf-8

# ### Marshmallow

# Marshmallow gets its name from "marshalling" - in other words it is a library that can be used to "translate" objects to and from complex data types (such as custom objects) and simple datatypes (such as dictionaries or lists of strings, integers, etc), sometimes called  native data types, which can then easily be serialized and deserialized into a JSON format.
# At the same time, it can also perform validation.
# 
# Marshmallow is very customizable, and I am not going to go into a whole lot of detail here, other than show you a few examples.
# 
# If you want more info about this great Python library, you can read up about it here: https://marshmallow.readthedocs.io/en/3.0/
# 

# As might be expected, we still declare some sort of schema for our data - there's no magic here!

# Let's first see how we might create a simple schema for our `Person` object.

# We start by creating the class itself that we will use in our app:

# In[1]:


class Person:
    def __init__(self, first_name, last_name, dob):
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        
    def __repr__(self):
        return f'Person({self.first_name}, {self.last_name}, {self.dob})'


# In[2]:


from datetime import date

p1 = Person('John', 'Cleese', date(1939, 10, 27))


# In[3]:


p1


# So we want to serialize and deserialize this `Person` object into a simple dictionary containing strings, including an ISO formatted string for the date of birth.

# In[4]:


from marshmallow import Schema, fields


# In[5]:


class PersonSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    dob = fields.Date()


# We can now create a schema instance that will handle any object type that has the `first_name`, `last_name` and `dob` fields. You'll notice that we used Marshmallow specific data types for strings and dates. Marshmallow has many other data types too to handle Booleans, numbers (integers, reals, even decimals), datetime, email, url, etc.

# We first have to create an instance of the `PersonSchema` class:

# In[6]:


person_schema = PersonSchema()


# We can serialize our custom object into a "simple" dictionary:

# In[7]:


person_schema.dump(p1)


# As you can see we have two properties here: `data` and `errors`. The `data` property will contain our serialized data, and the `errors` property will tell us if any errors were encountered while serializing our objects.

# In[8]:


type(person_schema.dump(p1).data)


# We can also serialize our objects directly to JSON using `dumps`:

# In[9]:


person_schema.dumps(p1).data


# We can use other objects, not necessarily of `Person` type, and if those fields are present they will be used in the serialization:

# In[10]:


from collections import namedtuple

PT=namedtuple('PT', 'first_name, last_name, dob')


# In[11]:


p2 = PT('Eric', 'Idle', date(1943, 3, 29))


# In[12]:


person_schema.dumps(p2).data


# But if we use an object that does not have the required fields:

# In[13]:


PT2 = namedtuple('PT2', 'first_name, last_name, age')
p3 = PT2('Michael', 'Palin', 75)


# In[14]:


person_schema.dumps(p3).data


# As you can see Marshmallow here only uses what it can.
# 
# What's interesting is that we can also specify what fields should occur in the deserialized output, using `only` to specify inclusions, or `exclude` to specify exclusions:

# In[15]:


person_partial = PersonSchema(only=('first_name', 'last_name'))


# In[16]:


person_partial.dumps(p1).data


# Equivalently:

# In[17]:


person_partial = PersonSchema(exclude=['dob'])


# In[18]:


person_partial.dumps(p1).data


# What happens if we have the wrong data type for those fields?

# In[19]:


p4 = Person(100, None, 200)


# In[20]:


person_schema.dumps(p4)


# As you can see, the `errors` property tells us that the data value could not be interpreted as a date.

# On the other hand the values `100` and `None` for the string values were fine - the integer was converted into a string, and the `None` value for `last_name` was retained.
# 
# Our schemas can also get more complicated, including sub-schemas based on other schemas.
# 
# For example, we can define a `Movie` schema that includes a movie title, year of release, and a list of actors:

# In[21]:


class Movie:
    def __init__(self, title, year, actors):
        self.title = title
        self.year = year
        self.actors = actors


# In[22]:


class MovieSchema(Schema):
    title = fields.Str()
    year = fields.Integer()
    actors = fields.Nested(PersonSchema, many=True)


# In[23]:


p1, p2


# In[24]:


parrot = Movie('Parrot Sketch', 1989, [p1, 
                                       Person('Michael', 
                                              'Palin', 
                                              date(1943, 5, 5))
                                      ])


# In[25]:


MovieSchema().dumps(parrot)


# There's a lot more we can do to control serialization - take a look at the documentation if you want to learn more.
# 
# Now, let's look at deserialization a little bit.

# To deserialize a simple dictionary we use the `load` method (deserializes a dictionary, the opposite of what `dump` does basically). We deserialize a JSON string using the `loads` method.

# Let's recall our Person schema:

# In[26]:


class PersonSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    dob = fields.Date()


# And let's deserialize a dictionary:

# In[27]:


person_schema = PersonSchema()


# In[28]:


person_schema.load(dict(first_name='John',
                        last_name='Cleese',
                        dob='1939-10-27'))


# So you can see we get this `UnmarshalResult` object back, with a `data` property - notice how the data was converted from a string into an actual date object.
# 
# But we still did not get a `Person` object back in `data`. Instead we got a plain dictionary back - ultimately we may want a `Person` object.
# 
# To do this, we need to tell Marshmallow what object to use when it deserializes our data:

# In[29]:


from marshmallow import post_load

class PersonSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    dob = fields.Date()
    
    @post_load
    def make_person(self, data):
        return Person(**data)


# In[30]:


person_schema = PersonSchema()


# In[31]:


person_schema.load(dict(first_name='John',
                        last_name='Cleese',
                        dob='1939-10-27'))


# And now you can see that `data` contains a `Person` object.

# So now let's go ahead and fix up our `MovieSchema` as well:

# In[32]:


class MovieSchema(Schema):
    title = fields.Str()
    year = fields.Integer()
    actors = fields.Nested(PersonSchema, many=True)
    
    @post_load
    def make_movie(self, data):
        return Movie(**data)


# In[33]:


movie_schema = MovieSchema()


# Here we're going to load from a JSON string to see that it works equally well:

# In[34]:


json_data = '''
{"actors": [
    {"first_name": "John", "last_name": "Cleese", "dob": "1939-10-27"}, 
    {"first_name": "Michael", "last_name": "Palin", "dob": "1943-05-05"}], 
"title": "Parrot Sketch", 
"year": 1989}
'''


# In[35]:


movie = movie_schema.loads(json_data).data


# In[36]:


type(movie)


# In[37]:


movie.title, movie.year


# In[38]:


movie.actors


# There is a **lot** more that this library can do - we did not even touch on validation here (required fields for example), nor how you can manipulate serialization and deserialization in many different ways, including handling of missing values, and much much more. If you are going to work with complex objects and have to deal with JSON (or other) marshalling, I strongly urge you to consider this library. It has a bit of a learning curve, but is well worth the effort!
# 
# There are others out there as well. `Colander`, part of the `Pyramid` project is also popular with people using `Pyramid`. Personally I just find `Marshmallow` more powerful and pleasant to work with.
