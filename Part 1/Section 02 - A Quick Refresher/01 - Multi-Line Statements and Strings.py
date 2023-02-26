#!/usr/bin/env python
# coding: utf-8

# ## Multi-Line Statements and Strings

# Certain physical newlines are ignored in order to form a complete logical 
# line of code.

# #### Implicit Examples

# In[1]:


a = [1, 
    2, 
    3]


# In[2]:


a


# You may also add comments to the end of each physical line:

# In[6]:


a = [1, #first element
    2, #second element
    3, #third element
    ]


# In[4]:


a


# Note if you do use comments, you must close off the collection on a new line.
# 
# i.e. the following will not work since the closing ] is actually part of the
# comment:

# In[7]:


#a = [1, # first element
    #2 #second element]


# This works the same way for tuples, sets, and dictionaries.

# In[8]:


a = (1, # first element
    2, #second element
    3, #third element
    )


# In[9]:


a


# In[10]:


a = {1, # first element
    2, #second element
    }


# In[11]:


a


# In[15]:


a = {'key1': 'value1', #comment,
    'key2': #comment
    'value2' #comment
    }


# In[13]:


a


# We can also break up function arguments and parameters:

# In[18]:


def my_func(a, #some comment
           b, c):
    print(a, b, c)


# In[19]:


my_func(10, #comment
       20, #comment
       30)


# #### Explicit Examples

# You can use the ``\`` character to explicitly create multi-line statements.

# In[23]:


a = 10
b = 20
c = 30
if a > 5 \
    and b > 10 \
    and c > 20:
    print('yes!!')


# The identation in continued-lines does not matter:

# In[22]:


a = 10
b = 20
c = 30
if a > 5 \
    and b > 10 \
        and c > 20:
    print('yes!!')


# #### Multi-Line Strings

# You can create multi-line strings by using triple delimiters (single or 
# double quotes)

# In[26]:


a = '''this is
a multi-line string'''


# In[27]:


print(a)


# Note how the newline character we typed in the multi-line string was preserved. Any character you type is preserved. You can also mix in escaped characters line any normal string.

# In[34]:


a = """some items:\n
    1. item 1
    2. item 2"""


# In[35]:


print(a)


# Be careful if you indent your multi-line strings - the extra spaces are preserved!

# In[41]:


def my_func():
    a = '''a multi-line string
    that is actually indented in the second line'''
    return a


# In[42]:


print(my_func())


# In[45]:


def my_func():
    a = '''a multi-line string
that is not indented in the second line'''
    return a


# In[46]:


print(my_func())


# Note that these multi-line strings are **not** comments - they are real strings
# and, unlike comments, are part of your compiled code. They are however sometimes
# used to create comments, such as ``docstrings``, that we will cover later in
# this course.

# In general, use ``#`` to comment your code, and use multi-line strings only when
# actually needed (like for docstrings).

# Also, there are no multi-line comments in Python. You simply have to use a ``#``
# on every line.

# In[47]:


# this is
#    a multi-line
#    comment


# The following works, but the above formatting is preferrable.

# In[55]:


# this is
    # a multi-line
    # comment

# Doc strings for functions, classes modules etc.
# Always use """ string regardless of the number of lines.
# Summary line, followed by a blank line and a more elaborate description.

def my_test_function_1(a, b):
    """This is a multiline docstring summary line
    
Followed by a more elaborate description after a single blank line.
Refer to PEPs 256 & 258
for a multi-line docstring put the closing triple quotes on their own line. 
"""
    print(f"This is the doc string:\n\n{my_test_function_1.__doc__}")



my_test_function_1(a, b)    
