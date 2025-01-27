#!/usr/bin/env python
# coding: utf-8

# ### Custom JSON Encoding using JSONEncoder

# In the previous video, we saw how we were able to provide custom encodings using the `default` argument of the `dump`/`dumps` function.
# 
# But how does Python know how to encode the "standard" types, such as `str`, `int`, `float`, `list`, `dict`, etc?
# 
# It uses a special class - `JSONEncoder`.
# 
# This class supports the following encodings (see Python docs: https://docs.python.org/3/library/json.html#json.JSONEncoder)

# |Python |JSON  |
# |:----|:---|
# | `dict` | object `{...}`|
# | `list`, `tuple` | array `[...]` |
# | `str`  | string `"..."`|
# | `int`, `float` | number |
# | `int` or `float` `Enums` | number |
# | `bool` | `true` or `false` |
# | `None` | `null` |

# Anything beyond those Python types and we end up with a `TypeError` exception.

# We can see how this class encodes objects by calling an instance of it directly:

# In[1]:


import json

default_encoder = json.JSONEncoder()
default_encoder.encode([1, 2, 3])


# And for non-supported objects:

# In[2]:


default_encoder.encode(1+1j)


# We can actually extend this `JSONEncoder` class and override the `default` method. We can then add in support for whatever type we want to use, and pass any other types to the parent class to handle (either serialize the data or raise a `TypeError` exception). 

# Let's just see a simple example first:

# In[3]:


import json
from datetime import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, arg):
        if isinstance(arg, datetime):
            return arg.isoformat()
        else:
            super().default(arg)


# In[4]:


custom_encoder = CustomJSONEncoder()


# In[5]:


custom_encoder.encode(True)


# In[6]:


custom_encoder.encode(datetime.utcnow())


# And we can now use this custom encoder by specifying it when we use `dump`/`dumps`:

# In[7]:


json.dumps(dict(name='test', time=datetime.utcnow()), cls=CustomJSONEncoder)


# One thing to note is that for both the `default` approach, and the `cls` approach, our method / encoder will only be used for types that Python cannot already serialize on its own (strings, integers, lists, etc).

# In[8]:


def custom_encoder(arg):
    print('Custom encoder called...')
    if isinstance(arg, str):
        return f'some string: {arg}'


# Here we want to "override" `dumps` default encoding behavior for strings:

# In[9]:


json.dumps({'name': 'Python'}, default=custom_encoder)


# As you can see, we cannot do that - because the argument is a "recognized" type (`str`), Python does not even call our `custom_encoder` function.
# 
# And the same happens when we override the `default` method in our custom `JSONEncoder` class.

# Let's look at the signature for `dumps`:

# In[10]:


help(json.dumps)


# And let's see the signature for `JSONEncoder`:

# In[11]:


help(json.JSONEncoder)


# Here we are particularly interested in the `__init__` method signature:

#  `__init__(self, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)`

# `dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw)`
You'll notice that there are quite a few arguments for both, most of which are common to both.

With the `dump`/`dumps` method, there are quite a few things we can configure that control the json encoding - if we want to use those tweaks in a consistent manner throughout our app, we need to remember to use them consistently every time we call the `dump`/`dumps` function.

Consider this example:
# In[12]:


d = {
    'a': float('inf'),
    'b': [1, 2, 3]
}


# In[13]:


d


# In[14]:


type(d['a'])


# As you can see, that float is a special type of float - it represents + infinity.

# Let's see if Python can encode that:

# In[15]:


json.dumps(d)


# Yes, it does - but notice the output, `Infinity`. Technically this is not JSON... (see https://tools.ietf.org/html/rfc4627 Section 2.4)

# So, if we want to be strict about this, and ensure we are not trying to serialize a value such as infinity, we would do this instead:

# In[16]:


json.dumps(d, allow_nan=False)


# And we get the desired result.
# 
# What about trying to encode an invalid key (from JSON's perspective)::

# In[17]:


d = {10: "int", 10.5: "float", 1+1j: "complex"}


# In[18]:


d


# These are all valid Python dictionary keys, but what happens with JSON encoding?

# In[19]:


json.dumps(d)


# As you can see we get an exception. We may want to simply ignore that exception and not include the offending key/value pair in our serialization:

# In[20]:


json.dumps(d, skipkeys=True)


# And now we no longer get an exception, and the complex key was simply skipped.

# We can even change how the serialization is rendered (which of course means we may no longer have actual JSON):

# In[21]:


d = {
    'name': 'Python',
    'age': 27,
    'created_by': 'Guido van Rossum',
    'list': [1, 2, 3]
}


# In[22]:


json.dumps(d)


# In[23]:


print(json.dumps(d, indent='---', separators=('', ' = ')))


# We can use this by the way, to create more compact JSON strings (uses less bytes):

# In[24]:


print(json.dumps(d))


# vs

# In[25]:


print(json.dumps(d, separators=(',', ':')))


# As you can see, all the whitespace is eliminated. For transmitting large JSON objects, that can make a (relatively small) difference in making the JSON more compact.

# So, if we want to consistently use the same values for all those tweaks, we have to consistently remember to set the arguments correctly in the `dump`/`dumps` functions.
# 
# Instead, we could create a custom JSONEncoder class that pre-sets all these things, and just use that encoder - simpler than remembering all those arguments and their correct values:

# In[26]:


class CustomEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(skipkeys=True, 
                         allow_nan=False, 
                         indent='---', 
                         separators=('', ' = ')
                        )
        
    def default(self, arg):
        if isinstance(arg, datetime):
            return arg.isoformat()
        else:
            return super().default(arg)


# In[27]:


d = {
    'time': datetime.utcnow(),
    1+1j: "complex",
    'name': 'Python'
}


# In[28]:


print(json.dumps(d, cls=CustomEncoder))


# Another thing I want to point out is that with both these methods we are not limited in what we emit as our JSON serialization.
# 
# For example, for a `datetime` object, we may want to emit not only the ISO formatted date, but maybe some additional fields, all nested within a JSON object:

# In[29]:


class CustomEncoder(json.JSONEncoder):
    def default(self, arg):
        if isinstance(arg, datetime):
            obj = dict(
                datatype="datetime",
                iso=arg.isoformat(),
                date=arg.date().isoformat(),
                time=arg.time().isoformat(),
                year=arg.year,
                month=arg.month,
                day=arg.day,
                hour=arg.hour,
                minutes=arg.minute,
                seconds=arg.second
            )
            return obj
        else:
            return super().default(arg)


# In[30]:


d = {
    'time': datetime.utcnow(),
    'message': 'Testing...'
}


# In[31]:


print(json.dumps(d, cls=CustomEncoder, indent=2))

