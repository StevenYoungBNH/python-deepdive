#!/usr/bin/env python
# coding: utf-8

# ### Attribute Write Accessors

# As we saw in the lecture there is one special method for attribute writes: `__setattribute__`.

# Let's just see when it gets called:

# In[1]:


class Person:
    def __setattr__(self, name, value):
        print('setting instance attribute...')
        super().__setattr__(name, value)


# In[2]:


p = Person()


# In[3]:


p.name = 'Guido'


# Of course, if we set a class attribute it does not get called:

# In[4]:


Person.class_attr = 'test'


# In order to override this setter for class attributes we would have to define it in the metaclass:

# In[5]:


class MyMeta(type):
    def __setattr__(self, name, value):
        print('setting class attribute...')
        return super().__setattr__(name, value)
    
class Person(metaclass=MyMeta):
    def __setattr__(self, name, value):
        print('setting instance attribute...')
        super().__setattr__(name, value)


# In[6]:


Person.test = 'test'


# In[7]:


p = Person()
p.test = 'test'


# And as we discussed in the lecture, if our `__setattr__` is setting a **data** descriptor, then it calls the descriptor's `__set__` method instead:

# In[8]:


class MyNonDataDesc:
    def __get__(self, instance, owner_class):
        print('__get__ called on non-data descriptor...')
        
class MyDataDesc:
    def __set__(self, instance, value):
        print('__set__ called on data descriptor...')
        
    def __get__(self, instance, owner_class):
        print('__get__ called on data descriptor...')


# In[9]:


class MyClass:
    non_data_desc = MyNonDataDesc()
    data_desc = MyDataDesc()
    
    def __setattr__(self, name, value):
        print('__setattr__ called...')
        super().__setattr__(name, value)


# In[10]:


m = MyClass()


# In[11]:


m.__dict__


# In[12]:


m.data_desc = 100


# In[13]:


m.non_data_desc = 200


# In[14]:


m.__dict__


# So `__setattr__` can be used to intercept and customize any attribute set operation on the instance that the method is defined for.

# Just as with `__getattr__` or `__getattribute__` we have to extra careful with infinite recursion.

# Suppose we want to disallow setting values for variables that start with a single underscore (but not a double underscore). We might try something like this:

# In[15]:


class MyClass:
    def __setattr__(self, name, value):
        print('__setattr__ called...')
        if name.startswith('_') and not name.startswith('__'):
            raise AttributeError('Sorry, this attribute is read-only.')
        setattr(self, name, value)


# In[16]:


m = MyClass()


# This works fine:

# In[17]:


try:
    m._test = 'test'
except AttributeError as ex:
    print(ex)


# But this will not:

# In[18]:


try:
    m.test = 'test'
except RecursionError as ex:
    print(ex)


# And of course this is because the line `self.name = value` we have in `__setattr__` is itself calling `__setattr__`. So instead, we have to delegate this back to the parent:

# In[19]:


class MyClass:
    def __setattr__(self, name, value):
        print('__setattr__ called...')
        if name.startswith('_') and not name.startswith('__'):
            raise AttributeError('Sorry, this attribute is read-only.')
        super().__setattr__(name, value)


# In[20]:


m = MyClass()


# In[21]:


m.test = 'test'


# In[22]:


m.__dict__


# So, just as with the getters, when we want to actually get to the attributes in our instance, we just need to distinguish wether we want the default way of getting/setting the attribute, or our custom override, and use `super()` accordingly. As long as you remember that, you should be fine :-)

# In[ ]:




