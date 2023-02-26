#!/usr/bin/env python
# coding: utf-8

# ### Deleting Properties

# Just like we can delete an attribute from an instance object, we can also delete a property from an instance object.
# 
# Note that this action simply runs the deleter method, but the property remains defined **on the class**. It does not remove the property from the class, instead it is generally used to remove the property value from the **instance**.

# Properties, like attributes, can be deleted by using the `del` keyword, or the `delattr` function.

# In[1]:


class Person:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        print('getting name property value...')
        return self._name
    
    def set_name(self, value):
        print(f'setting name property to {value}...')
        self._name = value
    
    def del_name(self):
        # delete the underlying data
        print('deleting name property value...')
        del self._name
        
    name = property(fget=get_name, fset=set_name, fdel=del_name, doc='Person name.')


# In[2]:


p = Person('Guido')


# In[3]:


p.name


# And the underlying `_name` property is in our instance dictionary:

# In[4]:


p.__dict__


# In[5]:


del p.name


# As we can see, the underlying `_name` attribute is no longer present in the instance dictionary:

# In[6]:


p.__dict__


# In[7]:


try:
    print(p.name)
except AttributeError as ex:
    print(ex)


# As you can see, the property deletion did not remove the property definition, that still exists.

# Alternatively, we can use the `delattr` function as well:

# In[8]:


p = Person('Raymond')


# In[9]:


delattr(p, 'name')


# And we can of course use the decorator syntax as well:

# In[10]:


class Person:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        print('getting name property value...')
        return self._name
    
    @name.setter
    def name(self, value):
        """Person name"""
        print(f'setting name property to {value}...')
        self._name = value
    
    @name.deleter
    def name(self):
        # delete the underlying data
        print('deleting name property value...')
        del self._name


# In[11]:


p = Person('Alex')


# In[12]:


p.name


# In[13]:


del p.name


# In[ ]:




