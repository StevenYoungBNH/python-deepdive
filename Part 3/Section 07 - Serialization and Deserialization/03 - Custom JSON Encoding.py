#!/usr/bin/env python
# coding: utf-8

# ### Custom JSON Serialization

# As we saw in the previous video, certain data types cannot be serialized to JSON using Python's defaults. 
# Here's a simple example of this:

# In[1]:


from datetime import datetime


# In[2]:


current = datetime.utcnow()


# In[3]:


current


# As we can see, this is a `datetime` object.

# Now let's try to serialize it to JSON:

# In[4]:


import json


# In[5]:


json.dumps(current)


# As we can see Python raises a `TypeError` exception, stating that `datetime` objects are not JSON serializable.
# 
# So, we'll need to come up with our own serialization format.
# 
# For datetimes, the most common format is the **ISO 8601** format - you can read up more about it here (https://en.wikipedia.org/wiki/ISO_8601), but basically the format is:
# 
# *YYYY-MM-DD* **T** *HH:MM:SS*

# There are some variations for encoding timezones, but to keep things simple I am going to use timezone naive timestamps, and just use UTC everywhere.

# We could use Python's string representation for datetimes:

# In[6]:


str(current)


# but this is not quite ISO-8601. We could write a custom formatter ourselves:

# In[7]:


def format_iso(dt):
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


# (If you want more info and options on date and time formatting/parsing using `strftime` and `strptime`, which essentially pass through to their `C` counterparts, you can see the Python docs here: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)

# In[8]:


format_iso(current)


# But Python actually provides us a function to do the same:

# In[9]:


current.isoformat()


# This is almost identical to our custom representation, but also includes fractional seconds. If you don't want fractional seconds in your representation, then you'll have to write some custom code like the one above.
# I'm just going to use Python's ISO-8601 representation.
# And now let's serialize our `datetime` object to JSON:

# In[10]:


log_record = {'time': datetime.utcnow().isoformat(), 'message': 'testing'}


# In[11]:


json.dumps(log_record)


# OK, this works, but this is far from ideal. Normally, our dictionary will contain the `datetime` object, not it's string representation.
# 
# For example, in the example I showed above, our record would likely be:

# In[12]:


log_record = {'time': datetime.utcnow(), 'message': 'testing'}


# The problem is that `log_record` is now not JSON serializable!
# 
# What we have to do is write custom code to replace non-JSON serializable objects in our dictionary with custom representations. This can quickly become tedious and unmanageable if we deal with many dictionaries, and arbitrary structures.
# 
# Fortunately, Python's `dump` and `dumps` functions have some ways for us to define general serializations for non-standard JSON objects.
# 
# The simplest way is to specify a function that `dump`/`dumps` will call when it encounters something it cannot serialize:

# In[13]:


def format_iso(dt):
    return dt.isoformat()


# In[14]:


json.dumps(log_record, default=format_iso)


# This will work even if we have more than one date in our dictionary:

# In[15]:


log_record = {
    'time1': datetime.utcnow(),
    'time2': datetime.utcnow(),
    'message': 'Testing...'
}


# In[16]:


json.dumps(log_record, default=format_iso)


# So this works, but what happens if we introduce another non-serializable object:

# In[17]:


log_record = {
    'time': datetime.utcnow(),
    'message': 'Testing...',
    'other': {'a', 'b', 'c'}
}


# In[18]:


json.dumps(log_record, default=format_iso)


# As you can see, Python encountered that `set`, and therefore called the `default` callable - but that callable was not designed to handle sets, and so we end up with an exception in the `format_iso` callable instead.
# 
# We can remedy this by essentially adding code to our function to make it handle various data types. Essentially creating a dispatcher - this should remind you of the single-dispatch generic function decorator available in the `functools` module which we discussed in an earlier part of this series. You can also view more info about it here: https://docs.python.org/3/library/functools.html#functools.singledispatch
# 

# Let's first write it without the decorator to make sure we have our code correct:

# In[19]:


def custom_json_formatter(arg):
    if isinstance(arg, datetime):
        return arg.isoformat()
    elif isinstance(arg, set):
        return list(arg)


# In[20]:


json.dumps(log_record, default=custom_json_formatter)


# To make things a little more interesting, let's throw in a custom object as well:

# In[21]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def toJSON(self):
        return {
            'name': self.name,
            'age': self.age,
            'create_dt': self.create_dt.isoformat()
        }


# In[22]:


p = Person('John', 82)
print(p)
print(p.toJSON())


# And we modify our custom JSON formatter as follows:

# In[23]:


def custom_json_formatter(arg):
    if isinstance(arg, datetime):
        return arg.isoformat()
    elif isinstance(arg, set):
        return list(arg)
    elif isinstance(arg, Person):
        return arg.toJSON()


# We can now serialize a more complex object:

# In[24]:


log_record = dict(time=datetime.utcnow(),
                  message='Created new person record',
                  person=p)


# In[25]:


json.dumps(log_record, default=custom_json_formatter)


# In[26]:


print(json.dumps(log_record, default=custom_json_formatter, indent=2))


# One thing to note here is that for the `Person` class we returned a formatted string for the `created_dt` attribute. We don't actually need to do this - we can simply return a `datetime` object and let `custom_json_formatter` handle serializing the `datetime` object:

# In[27]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def toJSON(self):
        return {
            'name': self.name,
            'age': self.age,
            'create_dt': self.create_dt
        }


# In[28]:


p = Person('Monty', 100)


# In[29]:


log_record = dict(time=datetime.utcnow(),
                  message='Created new person record',
                  person=p)


# In[30]:


print(json.dumps(log_record, default=custom_json_formatter, indent=2))


# In fact, we could simplify our class further by simply returning a dict of the attributes, since in this case we want to serialize everything as is.
# But using the `toJSON` callable means we can customize exactly how we want out objects to be serialized.
# 
# So, if we weren't particular about the serialization we could do this:

# In[31]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def toJSON(self):
        return vars(self)


# In[32]:


p = Person('Python', 27)


# In[33]:


p.toJSON()


# In[34]:


log_record['person'] = p
print(log_record)


# In[35]:


print(json.dumps(log_record, default=custom_json_formatter, indent=2))


# In fact, we could use this approach in our custom formatter - if an object does not have a `toJSON` callable, we'll just use a dictionary of the attributes - it it has any, it might not (like a complex number or a set as examples), so we need to watch out for that as well.

# In[36]:


'toJSON' in vars(Person)


# In[37]:


def custom_json_formatter(arg):
    if isinstance(arg, datetime):
        return arg.isoformat()
    elif isinstance(arg, set):
        return list(arg)
    else:
        try:
            return arg.toJSON()
        except AttributeError:
            try:
                return vars(arg)
            except TypeError:
                return str(arg)


# Let's create another custom class that does not have a `toJSON` method:

# In[38]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'


# In[39]:


pt1 = Point(10, 10)


# In[40]:


vars(pt1)


# In[41]:


log_record = dict(time=datetime.utcnow(),
                  message='Created new point',
                  point=pt1,
                  created_by=p)


# In[42]:


log_record


# And we can now serialize it to JSON:

# In[43]:


print(json.dumps(log_record, default=custom_json_formatter, indent=2))


# So now, let's re-write our custom json formatter using the generic single dispatch decorator I mentioned earlier:

# In[44]:


from functools import singledispatch


# Our default approach is going to first try to use `toJSON`, if not it will try to use `vars`, and it that still fails we'll use the string representation, whatever that happens to be:

# In[45]:


@singledispatch
def json_format(arg):
    print(arg)
    try:
        print('\ttrying to use toJSON...')
        return arg.toJSON()
    except AttributeError:
        print('\tfailed - trying to use vars...')
        try:
            return vars(arg)
        except TypeError:
            print('\tfailed - using string representation...')
            return str(arg)


# And now we 'register' other data types:

# In[46]:


@json_format.register(datetime)
def _(arg):
    return arg.isoformat()


# In[47]:


@json_format.register(set)
def _(arg):
    return list(arg)


# And we can now serialize just like before:

# In[48]:


print(json.dumps(log_record, default=json_format, indent=2))


# Let's change our Person class to emit some custom JSON instead of just using `vars`:

# In[49]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.create_dt = datetime.utcnow()
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def toJSON(self):
        return dict(name=self.name)


# In[50]:


p = Person('Python', 27)


# In[51]:


log_record['created_by'] = p


# In[52]:


print(json.dumps(log_record, default=json_format, indent=2))


# The way we wrote our default formatter, means that we can now also represent other unexpected data types, but using each object's string representation. If that's not acceptable, we can either not do this and let a `TypeError` exception get generated, or register more custom formatters:

# In[53]:


from decimal import Decimal
from fractions import Fraction

json.dumps(dict(a=1+1j, 
                b=Decimal('0.5'), 
                c=Fraction(1, 3),
                p=Person('Python', 27),
                pt=Point(0,0),
                time=datetime.utcnow()
               ), 
           default=json_format)


# Now, suppose we don't want that default representation for `Decimals` - we want to serialize it in this form: `Decimal(0.5)`.
# 
# All we need to do is to register a new function to serialize `Decimal` types:

# In[54]:


@json_format.register(Decimal)
def _(arg):
    return f'Decimal({str(arg)})'


# In[55]:


json.dumps(dict(a=1+1j, 
                b=Decimal(0.5), 
                c=Fraction(1, 3),
                p=Person('Python', 27),
                pt = Point(0,0),
                time = datetime.utcnow()
               ), 
           default=json_format)


# One last example that clearly shows the `json_format` function gets called recursively when needed:

# In[56]:


print(json.dumps(dict(pt = Point(Person('Python', 27), 2+2j)),
          default=json_format, indent=2))

