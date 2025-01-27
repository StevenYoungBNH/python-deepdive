#!/usr/bin/env python
# coding: utf-8

# ## Shared References and Mutability

# The following sets up a shared reference between the variables my_var_1 and my_var_2

# In[1]:


my_var_1 = 'hello'
my_var_2 = my_var_1
print(my_var_1)
print(my_var_2)


# In[2]:


print(hex(id(my_var_1)))
print(hex(id(my_var_2)))


# In[3]:


my_var_2 = my_var_2 + ' world!'


# In[4]:


print(hex(id(my_var_1)))
print(hex(id(my_var_2)))


# Be careful if the variable type is mutable!
# 
# Here we create a list (*my_list_1*) and create a variable (*my_list_2*) referencing the same list object:

# In[5]:


my_list_1 = [1, 2, 3]
my_list_2 = my_list_1
print(my_list_1)
print(my_list_2)


# As we can see they have the same memory address (shared reference):

# In[6]:


print(hex(id(my_list_1)))
print(hex(id(my_list_2)))


# Now we modify the list referenced by *my_list_2*:

# In[7]:


my_list_2.append(4)


# *my_list_2* has been modified:

# In[8]:


print(my_list_2)


# And since my_list_1 references the same list object, it has also changed:

# In[9]:


print(my_list_1)


# As you can see, both variables still share the same reference:

# In[10]:


print(hex(id(my_list_1)))
print(hex(id(my_list_2)))


# ### Behind the scenes with Python's memory manager
# ----

# Recall from a few lectures back:

# In[11]:


a = 10
b = 10


# In[12]:


print(hex(id(a)))
print(hex(id(b)))


# Same memory address!!
# 
# This is safe for Python to do because integer objects are **immutable**. 
# 
# So, even though *a* and *b* initially shared the same memory address, we can never modify *a*'s value by "modifying" *b*'s value. 
# 
# The only way to change *b*'s value is to change it's reference, which will never affect *a*.

# In[13]:


b = 15


# In[14]:


print(hex(id(a)))
print(hex(id(b)))


# However, for mutable objects, Python's memory manager does not do this, since that would **not** be safe.

# In[15]:


my_list_1 = [1, 2, 3]
my_list_2 = [1, 2 , 3]


# As you can see, although the two variables were assigned identical "contents", the memory addresses are not the same:

# In[16]:


print(hex(id(my_list_1)))
print(hex(id(my_list_2)))

