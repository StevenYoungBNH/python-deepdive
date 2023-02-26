#!/usr/bin/env python
# coding: utf-8

# ### The **operator** Module

# In[1]:


import operator


# In[2]:


dir(operator)


# #### Arithmetic Operators

# A variety of arithmetic operators are implemented.

# In[3]:


operator.add(1, 2)


# In[4]:


operator.mul(2, 3)


# In[5]:


operator.pow(2, 3)


# In[6]:


operator.mod(13, 2)


# In[7]:


operator.floordiv(13, 2)


# In[8]:


operator.truediv(3, 2)


# These would have been very handy in our previous section:

# In[9]:


from functools import reduce


# In[10]:


reduce(lambda x, y: x*y, [1, 2, 3, 4])


# Instead of defining a lambda, we could simply use **operator.mul**:

# In[11]:


reduce(operator.mul, [1, 2, 3, 4])


# #### Comparison and Boolean Operators

# Comparison and Boolean operators are also implemented as functions:

# In[12]:


operator.lt(10, 100)


# In[13]:


operator.le(10, 10)


# In[14]:


operator.is_('abc', 'def')


# We can even get the truthyness of an object:

# In[15]:


operator.truth([1,2])


# In[16]:


operator.truth([])


# In[17]:


operator.and_(True, False)


# In[18]:


operator.or_(True, False)


# #### Element and Attribute Getters and Setters

# We generally select an item by index from a sequence by using **[n]**:

# In[19]:


my_list = [1, 2, 3, 4]
my_list[1]


# We can do the same thing using:

# In[20]:


operator.getitem(my_list, 1)


# If the sequence is mutable, we can also set or remove items:

# In[21]:


my_list = [1, 2, 3, 4]
my_list[1] = 100
del my_list[3]
print(my_list)


# In[22]:


my_list = [1, 2, 3, 4]
operator.setitem(my_list, 1, 100)
operator.delitem(my_list, 3)
print(my_list)


# We can also do the same thing using the **operator** module's **itemgetter** function.
# 
# The difference is that this returns a callable:

# In[23]:


f = operator.itemgetter(2)


# Now, **f(my_list)** will return **my_list[2]**

# In[24]:


f(my_list)


# In[25]:


x = 'python'
f(x)


# Furthermore, we can pass more than one index to **itemgetter**:

# In[26]:


f = operator.itemgetter(2, 3)


# In[27]:


my_list = [1, 2, 3, 4]
f(my_list)


# In[28]:


x = 'pytyhon'
f(x)


# Similarly, **operator.attrgetter** does the same thing, but with object attributes.

# In[29]:


class MyClass:
    def __init__(self):
        self.a = 10
        self.b = 20
        self.c = 30
        
    def test(self):
        print('test method running...')


# In[30]:


obj = MyClass()


# In[31]:


obj.a, obj.b, obj.c


# In[32]:


f = operator.attrgetter('a')


# In[33]:


f(obj)


# In[34]:


my_var = 'b'
operator.attrgetter(my_var)(obj)


# In[35]:


my_var = 'c'
operator.attrgetter(my_var)(obj)


# In[36]:


f = operator.attrgetter('a', 'b', 'c')


# In[37]:


f(obj)


# Of course, attributes can also be methods.
# 
# In this case, **attrgetter** will return the object's **test** method - a callable that can then be called using **()**:

# In[38]:


f = operator.attrgetter('test')


# In[39]:


obj_test_method = f(obj)


# In[40]:


obj_test_method()


# Just like lambdas, we do not need to assign them to a variable name in order to use them:

# In[41]:


operator.attrgetter('a', 'b')(obj)


# In[42]:


operator.itemgetter(2, 3)('python')


# Of course, we can achieve the same thing using functions or lambdas:

# In[43]:


f = lambda x: (x.a, x.b, x.c)


# In[44]:


f(obj)


# In[45]:


f = lambda x: (x[2], x[3])


# In[46]:


f([1, 2, 3, 4])


# In[47]:


f('python')


# ##### Use Case Example: Sorting

# Suppose we want to sort a list of complex numbers based on the real part of the numbers:

# In[48]:


a = 2 + 5j
a.real


# In[49]:


l = [10+1j, 8+2j, 5+3j]
sorted(l, key=operator.attrgetter('real'))


# Or if we want to sort a list of string based on the last character of the strings:

# In[50]:


l = ['aaz', 'aad', 'aaa', 'aac']
sorted(l, key=operator.itemgetter(-1))


# Or maybe we want to sort a list of tuples based on the first item of each tuple:

# In[51]:


l = [(2, 3, 4), (1, 2, 3), (4, ), (3, 4)]
sorted(l, key=operator.itemgetter(0))


# #### Slicing

# In[52]:


l = [1, 2, 3, 4]


# In[53]:


l[0:2]


# In[54]:


l[0:2] = ['a', 'b', 'c']
print(l)


# In[55]:


del l[3:5]
print(l)


# We can do the same thing this way:

# In[56]:


l = [1, 2, 3, 4]


# In[57]:


operator.getitem(l, slice(0,2))


# In[58]:


operator.setitem(l, slice(0,2), ['a', 'b', 'c'])
print(l)


# In[59]:


operator.delitem(l, slice(3, 5))
print(l)


# #### Calling another Callable

# In[60]:


x = 'python'
x.upper()


# In[61]:


operator.methodcaller('upper')('python')


# Of course, since **upper** is just an attribute of the string object **x**, we could also have used:

# In[62]:


operator.attrgetter('upper')(x)()


# If the callable takes in more than one parameter, they can be specified as additional arguments in **methodcaller**:

# In[63]:


class MyClass:
    def __init__(self):
        self.a = 10
        self.b = 20
    
    def do_something(self, c):
        print(self.a, self.b, c)


# In[64]:


obj = MyClass()


# In[65]:


obj.do_something(100)


# In[66]:


operator.methodcaller('do_something', 100)(obj)


# In[67]:


class MyClass:
    def __init__(self):
        self.a = 10
        self.b = 20
    
    def do_something(self, *, c):
        print(self.a, self.b, c)


# In[68]:


obj.do_something(c=100)


# In[69]:


operator.methodcaller('do_something', c=100)(obj)


# More information on the **operator** module can be found here:
# 
# https://docs.python.org/3/library/operator.html
