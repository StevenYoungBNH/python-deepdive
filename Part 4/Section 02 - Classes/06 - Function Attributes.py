#!/usr/bin/env python
# coding: utf-8

# ### Function Attributes

# So far, we have been dealing with non-callable attributes. When attributes are actually functions, things behave differently.

# In[1]:


class Person:
    def say_hello():
        print('Hello!')


# In[2]:


Person.say_hello


# In[3]:


type(Person.say_hello)


# As we can see it is just a plain function, and be called as usual:

# In[4]:


Person.say_hello()


# Now let's create an instance of that class:

# In[5]:


p = Person()


# In[6]:


hex(id(p))


# We know we can access class attributes via the instance, so we should also be able to access the function attribute in the same way:

# In[7]:


p.say_hello


# In[8]:


type(p.say_hello)


# Hmm, the type has changed from `function` to `method`, and the function representation states that it is a **bound method** of the **specific object** `p` we created (notice the memory address).

# And if we try to call the function from the instance, here's what happens:

# In[9]:


try:
    p.say_hello()
except Exception as ex:
    print(type(ex).__name__, ex)


# `method` is an actual type in Python, and, like functions, they are callables, but they have one distinguishing feature. They need to be bound to an object, and that object reference is passed to the underlying function.
# 
# Often when we define functions in a class and call them from the instance we need to know which **specific** instance was used to call the function. This allows us to interact with the instance variables.
# 
# To do this, Python will automatically transform an ordinary function defined in a class into a method when it is called from an instance of the class.
# 
# Further, it will "bind" the method to the instance - meaning that the instance will be passed as the **first** argument to the function being called.
# 
# It does this using **descriptors** which we'll come back to in detail later.
# 
# For now let's just explore this a bit more:

# In[10]:


class Person:
    def say_hello(*args):
        print('say_hello args:', args)


# In[11]:


f'{hex(id(Person))}'


# In[12]:


Person.say_hello()


# As we can see, calling `say_hello` from the **class**, just calls the function (it is just a function).
# 
# But when we call it from an instance:

# In[12]:


p = Person()
hex(id(p))


# In[13]:


p.say_hello()


# You can see that the object `p` was passed as an argument to the class function `say_hello`.
# 
# The obvious advantage is that we can now interact with instance attributes easily:

# In[14]:


class Person:
    def set_name(instance_obj, new_name):
        instance_obj.name = new_name  # or setattr(instance_obj, 'name', new_name)
        


# In[15]:


p = Person()


# In[16]:


p.set_name('Alex')


# In[17]:


p.__dict__


# This has essentially the same effect as doing this:

# In[18]:


Person.set_name(p, 'John')


# In[19]:


p.__dict__


# By convention, the first argument is usually named `self`, but asd you just saw we can name it whatever we want - it just will be in the instance when the method variant of the function is called - and it is called an **instance method**.

# But **methods** are objects created by Python when calling class functions from an instance.
# 
# They have their own unique attributes too:

# In[20]:


class Person:
    def say_hello(self):
        print(f'{self} says hello')


# In[21]:


p = Person()


# In[22]:


p.say_hello


# In[23]:


m_hello = p.say_hello


# In[24]:


type(m_hello)


# For example it has a `__func__` attribute:

# In[25]:


m_hello.__func__


# which happens to be the class function used to create the method (the underlying function).

# But remember that a method is bound to an instance. In this case we got the method from the `p` object:

# In[26]:


hex(id(p))


# In[27]:


m_hello.__self__


# As you can see, the method also has a reference to the object it is **bound** to.

# So think of methods as functions that have been bound to a specific object, and that object is passed in as the first argument of the function call. The remaining arguments are then passed after that.

# Instance methods are created automatically for us, when we define functions inside our class definitions.
# 
# This even holds true if we monkey-patch our classes at run-time:

# In[28]:


class Person:
    def say_hello(self):
        print(f'instance method called from {self}')


# In[29]:


p = Person()
hex(id(p))


# In[30]:


p.say_hello()


# In[31]:


Person.do_work = lambda self: f"do_work called from {self}"


# In[32]:


Person.__dict__


# OK, so both functions are in the class `__dict__`.
# 
# let's create an instance and see what happens:

# In[33]:


p.say_hello


# In[34]:


p.do_work


# In[35]:


p.do_work()


# But be careful, if we add a function to the **instance** directly, this does not work the same - we have create a function in the instance, so it is not considered a method (since it was not defined in the class):

# In[36]:


p.other_func = lambda *args: print(f'other_func called with {args}')


# In[37]:


p.other_func


# In[38]:


'other_func' in Person.__dict__


# In[39]:


p.other_func()


# As you can see, `other_func` is, and behaves, like an ordinary function.

# Long story short, functions defined in a class are transformed into methods when called from instances of the class. So of course, we have to account for that extra argument that is passed to the method.

# In[ ]:




