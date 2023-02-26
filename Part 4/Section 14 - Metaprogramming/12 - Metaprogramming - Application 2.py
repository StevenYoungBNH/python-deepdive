#!/usr/bin/env python
# coding: utf-8

# ### Metaprogramming - Application 2

# There's another pattern we can implement using metaprogramming - Singletons.

# If you read online, you'll see that singleton objects are controversial in Python. 
# 
# I'm not going to get into a debate on this, other than to say I do not use singleton objects, not because I have deep thoughts about it (or even shallow ones for that matter), but rather because I have never had a need for them.

# However, the question often comes up, so here it is - the metaclass way of implementing the singleton pattern.
# 
# Whether you think you should use it or not, is entirely up to you!

# We have seen singleton objects - objects such as `None`, `True` or `False` for example.

# No matter where we create them in our code, they always refer to the **same** object.

# We can recover the type used to create `None` objects:

# In[361]:


NoneType = type(None)


# And now we can create multiple instances of that type:

# In[362]:


n1 = NoneType()
n2 = NoneType()


# In[363]:


id(n1), id(n2)


# As you can see, any instance of `NoneType` is actually the **same** object.

# The same holds true for booleans:

# In[364]:


b1 = bool([])
b2 = bool("")


# In[365]:


id(b1), id(b2)


# These are all examples of singleton objects. Now matter how we create them, we always end up with a reference to the same instance.

# There is no built-in mechanism to Python for singleton objects, so we have to do it ourselves.

# The basic idea is this:
# 
# When an instance of the class is being created (but **before** the instance is actually created), check if an instance has already been created, in which case return that instance, otherwise, create a new instance and store that instance reference somewhere so we can recover it the next time an instance is requested.

# We could do it entirely in the class itself, without any metaclasses, using the `__new__` method.
# 
# We can start with this:

# In[27]:


class Hundred:
    def __new__(cls):
        new_instance = super().__new__(cls)
        setattr(new_instance, 'name', 'hundred')
        setattr(new_instance, 'value', 100)
        return new_instance


# In[31]:


h1 = Hundred()


# In[32]:


vars(h1)


# But of course, this is not a singleton object.

# In[33]:


h2 = Hundred()


# In[34]:


h1 is h2


# So, let's fix this to make it a singleton:

# In[36]:


class Hundred:
    _existing_instance = None  # a class attribute!
    
    def __new__(cls):
        if not cls._existing_instance:
            print('creating new instance...')
            new_instance = super().__new__(cls)
            setattr(new_instance, 'name', 'hundred')
            setattr(new_instance, 'value', 100)
            cls._existing_instance = new_instance
        else:
            print('instance exists already, using that one...')
        return cls._existing_instance


# In[37]:


h1 = Hundred()


# In[38]:


h2 = Hundred()


# In[39]:


h1 is h2


# And there you are, we have a singleton object.

# So this works, but if you need to have multiple of these singleton objects, the code will just become repetitive.

# Metaclasses to the rescue!

# Remember what we are trying to do:
# 
# If we create two instances of our class `Hundred` we expect the same instance back.

# But how do we create an instance of a class - we **call** it, so `Hundred()`.

# Which `__call__` method is that? It is not the one in the `Hundred` class, that would make **instances** of `Hundred` callable, it is the `__call__` method in the **metaclass**.

# So, we need to override the `__call__` in our metaclass.

# In[84]:


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        print(f'Request received to create an instance of class: {cls}...')
        return super().__call__(*args, **kwargs)


# In[85]:


class Hundred(metaclass=Singleton):
    value = 100


# In[86]:


h = Hundred()


# In[87]:


h.value


# OK, that works, but now we need to make it into a singleton instance.

# We have to be careful here. Initially we had used the class itself (`Hundred`) to store, as a class variable, whether an instance had already been created. 
# 
# And here we could try to do the same thing. 
# 
# We could store the instance as a class variable in the class of the instance being created
# 
# That's actually quite simple, since the class is received as the first argument of the `__call__` method.

# In[100]:


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        print(f'Request received to create an instance of class: {cls}...')
        if getattr(cls, 'existing_instance', None) is None:
            print('Creating instance for the first time...')
            setattr(cls, 'existing_instance', super().__call__(*args, **kwargs))
        else:
            print('Using existing instance...')
        return getattr(cls, 'existing_instance')


# In[101]:


class Hundred(metaclass=Singleton):
    value = 100


# In[102]:


h1 = Hundred()


# In[103]:


h2 = Hundred()


# In[108]:


h1 is h2, h1.value, h2.value


# So that seems to work just fine. Let's create another singleton class and see if things still work.

# In[105]:


class Thousand(metaclass=Singleton):
    value = 1000


# In[106]:


t1 = Thousand()


# In[107]:


t2 = Thousand()


# In[109]:


h1 is h2, h1.value, h2.value


# In[110]:


t1 is t2, t1.value, t2.value


# In[111]:


h1 is t1, h2 is t2


# So far so good.

# Finally let's make sure everything works with **inheritance** too - if we inherit from a Singleton class, that subclass should also be a singleton.

# In[112]:


class HundredFold(Hundred):
    value = 100 * 100


# In[113]:


hf1 = HundredFold()


# Whaaat? Using existing instance? But this is the first time we created it!!

# The problem is this: How are we checking if an instance has already been created?

# We did this:
# ```if getattr(cls, 'existing_instance')```

# But since `HundredFold` inherits from `Hundred`, it also inherited the class attribute `existing_instance`.

# This means we have to be a bit more careful in our metaclass, we need to see if we have an instance of the **specific** class already created - and we cannot rely on storing a class attribute in the classes themselves since that breaks the pattern when subclassing.

# So, instead, we are going to store the class, and the instance of that class, in a dictionary **in the metaclass** itself, and use that dictionary to lookup the existing instance (if any) for a specific class.

# In[127]:


class Singleton(type):
    instances = {}
    
    def __call__(cls, *args, **kwargs):
        print(f'Request received to create an instance of class: {cls}...')
        existing_instance = Singleton.instances.get(cls, None)
        if existing_instance is None:
            print('Creating instance for the first time...')
            existing_instance = super().__call__(*args, **kwargs)
            Singleton.instances[cls] = existing_instance
        else:
            print('Using existing instance...')
        return existing_instance


# In[128]:


class Hundred(metaclass=Singleton):
    value = 100
    
class Thousand(metaclass=Singleton):
    value = 1000
    
class HundredFold(Hundred):
    value = 100 * 100


# In[129]:


h1 = Hundred()
h2 = Hundred()


# In[130]:


t1 = Thousand()
t2 = Thousand()


# In[131]:


hf1 = HundredFold()
hf2 = HundredFold()


# In[132]:


h1 is h2, t1 is t2, hf1 is hf2


# In[133]:


h1.value, h2.value, t1.value, t2.value, hf1.value, hf2.value


# And just to make sure :-)

# In[135]:


h1 is hf1

