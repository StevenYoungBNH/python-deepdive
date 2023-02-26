#!/usr/bin/env python
# coding: utf-8

# ### Project 1 - Solution

# In this project our goal is to validate one dictionary structure against a template dictionary.
# 
# A typical example of this might be working with JSON data inputs in an API. You are trying to validate this received JSON against some kind of template to make sure the received JSON conforms to that template (i.e. all the keys and structure are identical - value types being important, but not the value itself - so just the structure, and the data type of the values).
# 
# To keep things simple we'll assume that values can be either single values (like an integer, string, etc), or a dictionary, itself only containing single values or other dictionaries, recursively. In other words, we're not going to deal with lists as possible values. Also, to keep things simple, we'll assume that all keys are **required**, and that no extra keys are permitted.
# 
# In practice we would not have these simplifying assumptions, and although we could definitely write this ourselves, there are many 3rd party libraries that already exist to do this (such as `jsonschema`, `marshmallow`, and many more, some of which I'll cover lightly in some later videos.)

# For example you might have this template:

# In[1]:


template = {
    'user_id': int,
    'name': {
        'first': str,
        'last': str
    },
    'bio': {
        'dob': {
            'year': int,
            'month': int,
            'day': int
        },
        'birthplace': {
            'country': str,
            'city': str
        }
    }
}


# So, a JSON document such as this would match the template:

# In[2]:


john = {
    'user_id': 100,
    'name': {
        'first': 'John',
        'last': 'Cleese'
    },
    'bio': {
        'dob': {
            'year': 1939,
            'month': 11,
            'day': 27
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Weston-super-Mare'
        }
    }
}


# But this one would **not** match the template (missing key):

# In[3]:


eric = {
    'user_id': 101,
    'name': {
        'first': 'Eric',
        'last': 'Idle'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 3,
            'day': 29
        },
        'birthplace': {
            'country': 'United Kingdom'
        }
    }
}


# And neither would this one (wrong data type):

# In[4]:


michael = {
    'user_id': 102,
    'name': {
        'first': 'Michael',
        'last': 'Palin'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 'May',
            'day': 5
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Sheffield'
        }
    }
}


# Write a function such this:

# In[5]:


def validate(data, template):
    # implement
    # and return True/False
    # in the case of False, return a string describing 
    # the first error encountered
    # in the case of True, string can be empty
    return state, error


# That should return this:
# * `validate(john, template) --> True, ''`
# * `validate(eric, template) --> False, 'mismatched keys: bio.birthplace.city'`
# * `validate(michael, template) --> False, 'bad type: bio.dob.month'`

# ##### Solution

# There are many ways to approach this, but a recursive approach here will probably be simpler (not simple, just simpl**er**!) since we want to write a function that does not make any assumptions about how many dictionaries are nested.

# My approach is going to be as follows:
# 1. Write a recursive function
# 2. Maintain a breadcrumb (or *path*) of where we're at in the nested dictionaries (e.g. `bio.birthplace`)
# 3. Check to make sure all the required keys from the template are present in the data (for the same level)
# 4. For dictionary valued keys, recursively call my function
# 5. For non-dictionary values make sure they are of the correct type

# I'm going to build this function up little by little.
# 
# Let's first start by determining if we have mismatched keys: missing keys required by template, or extra keys in data not specified by template:

# In[6]:


def match_keys(data, valid, path):
    # path is just a string containing the current path
    # that we can use to append the extra/missing keys
    # and create a full path for the mismatched keys
    data_keys = data.keys()
    valid_keys = valid.keys()
    # we could just use data_keys ^ valid_keys
    # to get mismatched keys, but I prefer to differentiate
    # between missing and extra keys separately
    extra_keys = data_keys - valid_keys
    missing_keys = valid_keys - data_keys
    # Finally, build up the error state and message
    if missing_keys or extra_keys:
        is_ok = False
        missing_msg = ('missing keys:' +
                       ','.join({path + '.' + str(key) 
                                 for key in missing_keys})
                      ) if missing_keys else ''
        extras_msg = ('extra keys:' + 
                     ','.join({path + '.' + str(key) 
                               for key in extra_keys})
                     ) if extra_keys else ''
        return False, ' '.join((missing_msg, extras_msg))
    else:
        return True, None


# Let's test this function out:

# In[7]:


t = {'a': int, 'b': int, 'c': int, 'd': int}
d = {'a': 'wrong type', 'b': 100, 'c': 200, 'd': {'wrong': 'type'}}
is_ok, err_msg = match_keys(d, t, 'some.path')
print(is_ok, err_msg)


# In[8]:


d = {'a': 'test', 'b': 'test', 'c': 'test'}
is_ok, err_msg = match_keys(d, t, 'some.path')
print(is_ok, err_msg)


# In[9]:


d = {'a': 'test', 'b': 'test', 'c': 'test', 'd': 'test', 'z': 'extra'}
is_ok, err_msg = match_keys(d, t, 'some.path')
print(is_ok, err_msg)


# In[10]:


d = {'a': 'test', 'b': 'test', 'z': 'extra'}
is_ok, err_msg = match_keys(d, t, 'some.path')
print(is_ok, err_msg)


# OK, so now let's write a function that matches the types of corresponding (could be an actual type, or a nested dictionary):

# In[11]:


def match_types(data, template, path):
    # assume here that the keys have already been matched OK
    # but do not assume that the keys are necessarily in the same
    # order in both the data and the template
    for key, value in template.items():
        if isinstance(value, dict):
            template_type = dict
        else:
            template_type = value
        data_value = data.get(key, object())
        if not isinstance(data_value, template_type):
            err_msg = ('incorrect type: ' + path + '.' + key +
                       ' -> expected ' + template_type.__name__ +
                       ', found ' + type(data_value).__name__)
            return False, err_msg
    return True, None        


# Let's test this one out:

# In[12]:


t = {'a': int, 'b': str, 'c': {'d': int}}
d = {'a': 100, 'b': 'test', 'c': {'some': 'dict'}}
match_types(d, t, 'some.path')


# In[13]:


d = {'a': 100, 'b': 'test', 'c': 'unexpected'}
match_types(d, t, 'some.path')


# In[14]:


d = {'a': 100, 'b': 200, 'c': {'some': 'dict'}}
match_types(d, t, 'some.path')


# OK, so far so good!

# Now it's time to combine these into our main recursive function:

# In[15]:


def recurse_validate(data, template, path):
    # validate keys match
    is_ok, err_msg = match_keys(data, template, path)
    if not is_ok:
        return False, err_msg

    # validate individual data types match
    is_ok, err_msg = match_types(data, template, path)
    if not is_ok:
        return False, err_msg
    
    # Now see if we have nested dictionaries in template
    # (or data, since we know both keys and value data types match)
    dictionary_type_keys = {key for key, value in template.items()
                           if isinstance(value, dict)}
    for key in dictionary_type_keys:
        sub_path = path + '.' + str(key)
        sub_template = template[key]
        sub_data = data[key]
        is_ok, err_msg = recurse_validate(sub_data, sub_template, sub_path)
        if not is_ok:
            return False, err_msg
        
    return True, None


# Now let's test this function:

# In[16]:


is_ok, err_msg = recurse_validate(john, template, 'root')
print(is_ok, err_msg)


# In[17]:


is_ok, err_msg = recurse_validate(eric, template, 'root')
print(is_ok, err_msg)


# In[18]:


is_ok, err_msg = recurse_validate(michael, template, 'root')
print(is_ok, err_msg)


# Nice, now all that's left is to write our main function - it's only role really is to hide the recursive function from the caller, and provide a "start" path (which should be empty):

# In[19]:


def validate(data, template):
    return recurse_validate(data, template, '')


# In[20]:


persons = ((john, 'John'), (eric, 'Eric'), (michael, 'Michael'))


# In[21]:


for person, name in persons:
    is_ok, err_msg = validate(person, template)
    print(f'{name}: valid={is_ok}: {err_msg}')


# As an additional tweak, I'm not going to return a tuple with the sate and the error message, instead I'm going to use exceptions to do the same thing:

# In[22]:


class SchemaError(Exception):
    pass

def validate(data, template):
    is_ok, err_msg = recurse_validate(data, template, '')
    if not is_ok:
        raise SchemaError(err_msg)


# Then we can use the validator this way:

# In[23]:


validate(john, template)


# In[24]:


validate(eric, template)


# In[25]:


validate(michael, template)


# Of course, we could use this approach throughout instead of returning a status and an exception - this would make this a bit cleaner, and we can also differentiate between key mismatches vs value mismatches:

# In[26]:


class SchemaError(Exception):
    pass

class SchemaKeyMismatch(SchemaError):
    pass

class SchemaTypeMismatch(SchemaError, TypeError):
    pass


# In[27]:


def match_keys(data, valid, path):
    # path is just a string containing the current path
    # that we can use to append the extra/missing keys
    # and create a full path for the mismatched keys
    data_keys = data.keys()
    valid_keys = valid.keys()
    # we could just use data_keys ^ valid_keys
    # to get mismatched keys, but I prefer to differentiate
    # between missing and extra keys separately
    extra_keys = data_keys - valid_keys
    missing_keys = valid_keys - data_keys
    # Finally, build up the error state and message
    if missing_keys or extra_keys:
        is_ok = False
        missing_msg = ('missing keys:' +
                       ','.join({path + '.' + str(key) 
                                 for key in missing_keys})
                      ) if missing_keys else ''
        extras_msg = ('extra keys:' + 
                     ','.join({path + '.' + str(key) 
                               for key in extra_keys})
                     ) if extra_keys else ''
        raise SchemaKeyMismatch(' '.join((missing_msg, extras_msg)))


# In[28]:


def match_types(data, template, path):
    # assume here that the keys have already been matched OK
    # but do not assume that the keys are necessarily in the same
    # order in both the data and the template
    for key, value in template.items():
        if isinstance(value, dict):
            template_type = dict
        else:
            template_type = value
        data_value = data.get(key, object())
        if isinstance(data_value, template_type):
            continue
        else:
            err_msg = ('incorrect type: ' + path + '.' + key +
                       ' -> expected ' + template_type.__name__ +
                       ', found ' + type(data_value).__name__)
            raise SchemaTypeMismatch(err_msg)


# In[29]:


def recurse_validate(data, template, path):
    match_keys(data, template, path)
    match_types(data, template, path)

    # Now see if we have nested dictionaries in template
    # (or data, since we know both keys and value data types match)
    dictionary_type_keys = {key for key, value in template.items()
                           if isinstance(value, dict)}
    for key in dictionary_type_keys:
        sub_path = path + '.' + str(key)
        sub_template = template[key]
        sub_data = data[key]
        recurse_validate(sub_data, sub_template, sub_path)


# In[30]:


def validate(data, template):
    recurse_validate(data, template, '')


# In[31]:


validate(john, template)


# In[32]:


validate(eric, template)


# In[33]:


validate(michael, template)


# The nice thing about the way we have structured our exceptions is that we can catch them either as specific `SchemaKeyMismatch` or `SchemaTypeMismatch` exceptions, but also more broadly as `SchemaError` exceptions:

# In[34]:


try:
    validate(eric, template)
except SchemaError as ex:
    print(ex)


# In[35]:


try:
    validate(eric, template)
except SchemaKeyMismatch as ex:
    print('mismatched keys, doing some specific handling for that')
    print(ex)
except SchemaTypeMismatch as ex:
    print('mismatched types, doing some specific handling for that')
    print(ex)


# In[36]:


try:
    validate(michael, template)
except SchemaKeyMismatch as ex:
    print('mismatched keys, doing some specific handling for that')
    print(ex)
except SchemaTypeMismatch as ex:
    print('mismatched types, doing some specific handling for that')
    print(ex)

