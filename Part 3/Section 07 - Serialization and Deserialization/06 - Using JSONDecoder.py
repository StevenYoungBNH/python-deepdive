#!/usr/bin/env python
# coding: utf-8

# ### Using JSONDecoder

# Just like we can use a subclass of `JSONEncoder` to customize our json encodings, we can use a subclass of the default `JSONDecoder` class to customize decoding our json strings.

# It works quite differently from the `JSONEncoder` subclassing though.
#
# When we subclass `JSONEncoder` we override the `default` method which then allows us to intercept encoding of specific types of objects, and delegate back to the parent class what we don't want to handle specifically.
#
# With the `JSONDecoder` class we override the `decode` function which passes us the **entire** JSON as a **string** and we have to return whatever Python object we want. There's no delegating anything back to the parent class unless we want to completely skip customizing the output.

# Let's first see how the functions work:

# In[1]:


import json


# In[2]:


j = '''
    {
        "a": 100,
        "b": [1, 2, 3],
        "c": "python",
        "d": {
            "e": 4,
            "f": 5.5
        }
    }
'''


# In[3]:


class CustomDecoder(json.JSONDecoder):
    def decode(self, arg):
        print("decode:", type(arg), arg)
        return "a simple string object"


# In[4]:


print(json.loads(j, cls=CustomDecoder))


# As you can see, whatever we return from the `decode` method is the **result** of calling `loads`.
#
# So, we might want to intercept certain JSON strings, handling them in some custom way, and delegate back to the parent class if it's not a string we want to handle ourselves - but it's all or nothing:

# Let's see an example of how we might want to use this:

# In[5]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'


# In[6]:


j_points = '''
{
    "points": [
        [10, 20],
        [-1, -2],
        [0.5, 0.5]
    ]
}
'''

j_other = '''
{
    "a": 1,
    "b": 2
}
'''


# In[7]:


class CustomDecoder(json.JSONDecoder):
    def decode(self, arg):
        if 'points' in arg:
            obj = json.loads(arg)
            print("obj:", obj)
            return "parsing object for points"
        else:
            return super().decode(arg)


# In[8]:

print(j_points)
print(json.loads(j_points, cls=CustomDecoder))


# In[9]:

print(j_other)
print(json.loads(j_other, cls=CustomDecoder))


# So, let's implement the custom decoder now, assuming that `points` will be a top level node in the JSON object:

# In[10]:


class CustomDecoder(json.JSONDecoder):
    def decode(self, arg):
        obj = json.loads(arg)
        print("obj before:", obj)
        if 'points' in obj:  # top level
            obj['points'] = [Point(x, y)
                             for x, y in obj['points']]
        print("obj after:", obj)
        return obj


# In[11]:


print(json.loads(j_points, cls=CustomDecoder))


# In[12]:


print(json.loads(j_other, cls=CustomDecoder))


# Of course, we can be more fancy and maybe handle points by specifying the data type in the JSON object (and again, this is just how **we**, the developer, decide to make that specification).
#
# Here I am going to specify that a `Point` object in the JSON document should be specified using this format:
#
# ```
# {"_type": "point", "x": x-coord, "y": y-coord}
# ```

# So, when we parse the JSON string we are going to look for such a structure, and do the appropriate type conversion if needed. Of course, we'll have to look recursively in the JSON for this structure. We'll follow the same approach as before, first deserializing to a "generic" Python dict, then replacing any `Point` structure as we find them.

# To avoid having to iterate through the deserialized JSON object when we don't have that structure there in the first place, I'm going to look for `"_type": "point"` in the **string**. Technically we also need to look for `"_type":"point"` since both, from a JSON object perspective, are the same thing.
# In fact any amount of whitespace surrounding the `:` is acceptable. It would be possible but result in very unwieldy and concoluted code if we were to use an ordinary string search, so I'm going to use a regular expression instead (if you need help getting started with regular expressions, I highly recommend using this site:
#
# https://regexr.com/

# In[13]:


import re
pattern = r'"_type"\s*:\s*"point"'


# In this pattern, `\s` simply means a whitespace character, and the `*` right after it means zero or more times.
#
# Also note that we prefix that string with `r` to tell Python not to interpret the `\` as anything special - otherwise Python will try to escape that, or interpet it, when conbined with another character, as an escape sequence.
#
# Let's see a quick example of this first:

# In[14]:


print('word1\tword2')


# In[15]:


print(r'word1\tword2')


# Notice the difference? Since we use the `\` character a lot in regular expressions, we should always use this `r` prefix which indicates a **raw** string, and Python will not try to recognize escape sequences in our pattern.
#
# So, now let's continue testing out our regular expression pattern. We'll compile it so we can re-use it, but you dont have to.
#
# Once we have it compiled, we can use the `search` method that will find the first occurrence of the pattern in our search string, or return `None` if it was not found:

# In[16]:


regexp = re.compile(pattern)


# In[17]:


print(regexp.search('"a": 1'))


# In[18]:


print(regexp.search('"_type": "point"'))


# In[19]:


print(regexp.search('"_type"   : "point"'))


# Alternatively, if we don't want to compile it (if we only use it once, there's no real need to do so), we can do a search this way:

# In[20]:


re.search(pattern, '"_type"  :  "point"')


# OK, now that we have a working regular expression pattern we can implement our custom JSON decoder.

# In[21]:


class CustomDecoder(json.JSONDecoder):
    def decode(self, arg):
        obj = json.loads(arg)
        print("obj before:", obj)
        pattern = r'"_type"\s*:\s*"point"'
        if re.search(pattern, arg):
            # we have at least one `Point'
            obj = self.make_pts(obj)
        print("obj after:", obj)
        return obj

    def make_pts(self, obj):
        # recursive function to find and replace points
        # received object could be a dictionary, a list, or a simple type
        if isinstance(obj, dict):
            # first see if this dictionary is a point itself
            if '_type' in obj and obj['_type'] == 'point':
                # could have used: if obj.get('_type', None) == 'point'
                obj = Point(obj['x'], obj['y'])
            else:
                # root object is not a point
                # but it could contain a sub-object which itself
                # is or contains a Point object
                for key, value in obj.items():
                    obj[key] = self.make_pts(value)
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                obj[index] = self.make_pts(item)
        return obj


# In[22]:


j = '''
{
    "a": 100,
    "b": 0.5,
    "rectangle": {
        "corners": {
            "b_left": {"_type": "point", "x": -1, "y": -1},
            "b_right": {"_type": "point", "x": 1, "y": -1},
            "t_left": {"_type": "point", "x": -1, "y": 1},
            "t_right": {"_type": "point", "x": 1, "y": 1}
        },
        "rotate": {"_type" : "point", "x": 0, "y": 0},
        "interior_pts": [
            {"_type": "point", "x": 0, "y": 0},
            {"_type": "point", "x": 0.5, "y": 0.5}
        ]
    }
}
'''


# In[23]:


print(json.loads(j))


# In[24]:


from pprint import pprint
pprint(json.loads(j, cls=CustomDecoder))


# The `JSONDecoder` class also has arguments such as `parse_int`, `parse_float`, etc we saw in the previous lecture.
# We can use those to define a custom `JSONEncoder` class if we wanted to - let's say we want to use `Decimals` instead of floats - just like before, but instead of specifying this each and every time we calls `loads`, we can bundle this up into a custom decoder instead:

# In[25]:


from decimal import Decimal
CustomDecoder = json.JSONDecoder(parse_float=Decimal)


# In[26]:


d = CustomDecoder.decode(j)


# In[27]:


pprint(d)


# Of course, we can combine this with our custom decoder too:

# In[28]:


class CustomDecoder(json.JSONDecoder):
    base_decoder = json.JSONDecoder(parse_float=Decimal)

    def decode(self, arg):
        obj = self.base_decoder.decode(arg)
        pattern = r'"_type"\s*:\s*"point"'
        if re.search(pattern, arg):
            # we have at least one `Point'
            obj = self.make_pts(obj)
        return obj

    def make_pts(self, obj):
        # recursive function to find and replace points
        # received object could be a dictionary, a list, or a simple type
        if isinstance(obj, dict):
            # first see if this dictionary is a point itself
            if '_type' in obj and obj['_type'] == 'point':
                obj = Point(obj['x'], obj['y'])
            else:
                # root object is not a point
                # but it could contain a sub-object which itself
                # is or contains a Point object nested at some level
                # maybe another dictionary, or a list
                for key, value in obj.items():
                    obj[key] = self.make_pts(value)
        elif isinstance(obj, list):
            # received a list - need to run each item through make_pts
            for index, item in enumerate(obj):
                obj[index] = self.make_pts(item)
        return obj


# In[29]:


print(json.loads(j, cls=CustomDecoder))


# It's not evident that our `Point(x=0.5, y=0.5)` actually contains `Decimal` objects - that's really just the string representation - so let's just make sure they are indeed `Decimal` objects:

# In[30]:


result = json.loads(j, cls=CustomDecoder)
pt = result['rectangle']['interior_pts'][1]
print("pt:", pt)
print(type(pt.x), type(pt.y))


# As you can see, decoding JSON into custom objects is not exactly easy - the basic reason being that JSON does not support anything other than simple data types such as integers, floats, strings, booleans, constants and objects and lists.
#
# The rest is up to us.
#
# This is one of the reasons there are quite a few 3rd party libraries that allow us to serialize and deserialize JSON objects that follow a certain schema.
#
# I'll discuss some of those in upcoming lectures.

# In[ ]:




