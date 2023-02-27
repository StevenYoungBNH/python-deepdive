#!/usr/bin/env python
# coding: utf-8

# ### Class Decorators

# Let's come back to decorators.
#
# So far, we have been using decorators to decorate functions - but of course,
# we could also use them to decorate classes:

# Let's start with a simple example first, like we saw in the lecture:

# In[1]:


import inspect
from functools import wraps


def savings(cls):
    cls.account_type = 'savings'
    return cls


def checking(cls):
    cls.account_type = 'checking'
    return cls


# In[2]:


class Account:
    pass


@savings
class Bank1Savings(Account):
    pass


@savings
class Bank2Savings(Account):
    pass


@checking
class Bank1Checking(Account):
    pass


@checking
class Bank2Checking(Account):
    pass


# And if we inspect our classes, we'll see that the `account_type` attribute has
# been injected by the decorator:

# In[3]:


print(Bank1Savings.account_type, Bank1Checking.account_type)


# Of course, we could make even this simple example a little DRYer, by making a
# parameterized decorator:

# In[4]:


def account_type(type_):
    def decorator(cls):
        cls.account_type = type_
        return cls
    return decorator


# In[5]:


@account_type('Savings')
class Bank1Savings:
    pass


@account_type('Checking')
class Bank1Checking:
    pass


# In[6]:


print(Bank1Savings.account_type, Bank1Checking.account_type)


# We're not restricted to just adding data attributes either.

# Let's create a class decorator to inject a new function into the class before
# we return it:

# In[7]:


def hello(cls):
    cls.hello = lambda self: f'{self} says hello!'
    return cls


# In[8]:


@hello
class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# In[9]:


print(vars(Person))


# As you can see, the `Person` class now has an attribute `hello` which is a function.

# So, it will then become a bound method when we call it from an instance of
# `Person`:

# In[10]:


p = Person('Guido')


# In[11]:


print(p.hello())


# These examples are simple enough to understand what's going on, but not very
# useful.

# But we can do some interesting things.

# For example, suppose we want to log every call to every callable in some class.
#
# We could certainly do it this way:

# In[12]:


def func_logger(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(f'log: {fn.__qualname__}({args}, {kwargs}) = {result}')
        return result
    return inner


# In[13]:


class Person:
    @func_logger
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @func_logger
    def greet(self):
        return f'Hello, my name is {self.name} and I am {self.age}'


# In[14]:


p = Person('John', 78)


# In[15]:


print(p.greet())


# But this is kind of tedious if we have many methods in our class. Not very DRY!

# Instead, how about creating a class decorator that will decorate every callable
# in a given class with the logger decorator:
#
# sy 1/8/2003 As of Python 3.10 static methods are now callable. 
# In[16]:


def class_logger(cls):
    for name, obj in vars(cls).items():
        if callable(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))
    return cls


# So now we could do this:

# In[17]:


@class_logger
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f'Hello, my name is {self.name} and I am {self.age}'


# In[18]:


print(vars(Person))


# In[19]:


p = Person('John', 78)


# In[20]:


print(p.greet())


# Now we have to be a bit careful. Although this class decorator seems to work
# fine, it will have issues with static and class methods!
# static method is callable while class method is not callable
# In[21]:


@class_logger
class Person:
    @staticmethod
    def static_method():
        print('static_method invoked...')

    @classmethod
    def cls_method(cls):
        print(f'cls_method invoked for {cls}...')

    def instance_method(self):
        print(f'instance_method invoked for {self}')


# In[22]:


print(Person.static_method())


# In[23]:


print(Person.cls_method())


# In[24]:


print(Person().instance_method())


# You'll notice that in the `cls_method` and `instance_method` cases, the logger
# printout never showed up! In fact, we did not get the message that these
# methods had been decorated.

# What happened?

# The problem is that static and class methods are not functions, they are
# actually descriptors, not callables.

# In[25]:


class Person:
    @staticmethod
    def static_method():
        pass


print(Person.__dict__['static_method'])


# In[27]:


print(callable(Person.__dict__['static_method']))


# So, they were not decorated at all.

# Which is probably a good thing, because our decorator is expecting to decorate
# a function, not a class!

# This, by the way, is why when you decorate static or class methods using a
# function decorator in your classes, you should do so before you decorate it
# with the `@staticmethod` or `@classmethod` decorators:

# In[28]:


class Person:
    @staticmethod
    @func_logger
    def static_method():
        pass


# In[29]:


print(Person.static_method())


# But if you try it this way around, things aren't so happy:

# In[30]:


class Person:
    @func_logger
    @staticmethod
    def static_method():
        pass


# In[31]:


print(Person.static_method())


# We can actually fix this problem in our class decorator if we really wanted to.

# Let's first examine two things separately.
#
# First let's make sure we can recognize the type of a class or static method in
# our class:

# In[32]:


class Person:
    @staticmethod
    def static_method():
        pass

    @classmethod
    def class_method(cls):
        pass


# In[33]:


print(type(Person.__dict__['static_method']))


# In[34]:


print(type(Person.__dict__['class_method']))


# Next, can we somehow get back to the original function that was wrapped by the
# `@staticmethod` and `@classmethod` decorators?

# The answer is yes, since these are method objects - we've seen this before when
# we studied the relationship between functions and descriptors and how methods
# were created.

# In[35]:


print(Person.__dict__['static_method'].__func__)


# In[36]:


print(Person.__dict__['class_method'].__func__)


# So now, we could modify our class decorator needs to unwrap any class or static
# methods, decorate the original function, and then re-wrap it with the
# appropriate `classmethod` or `instancemethod` decorator:

# In[37]:


def class_logger(cls):
    for name, obj in vars(cls).items():
       
        if isinstance(obj, staticmethod):
            original_func = obj.__func__
            print('decorating static method', original_func)
            print(f'staticmethod is callable: {callable(obj)}')
            decorated_func = func_logger(original_func)
            method = staticmethod(decorated_func)
            print(method, type(method))
            setattr(cls, name, method)
        elif isinstance(obj, classmethod):
            original_func = obj.__func__
            print('decorating class method', original_func)
            print(f'classmethod is callable: {callable(obj)}')
            decorated_func = func_logger(original_func)
            method = classmethod(decorated_func)
            setattr(cls, name, method)
        elif callable(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))            
    return cls


# In[38]:


@class_logger
class Person:
    @staticmethod
    def static_method(a, b):
        print('static_method called...', a, b)

    @classmethod
    def class_method(cls, a, b):
        print('class_method called...', cls, a, b)

    def instance_method(self, a, b):
        print('instance_method called...', self, a, b)


# In[39]:


print(Person.static_method(10, 20))


# In[40]:


print(Person.class_method(10, 20))


# In[41]:


print(Person().instance_method(10, 20))


# Not bad... Not what about properties?

# In[42]:


@class_logger
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


# Hmm, the property was not decorated...

# Let's see what the type of that property is (you should already know this):

# In[43]:


print(type(Person.__dict__['name']))


# In[44]:


print(isinstance(Person.__dict__['name'], property))


# And how do we get the original functions on a property?

# In[45]:


prop = Person.__dict__['name']


# In[46]:


print(prop.fget)


# In[47]:


print(prop.fset, prop.fdel)


# Hmm, so maybe we can decorate the `fget`, `fset`, and `fdel` functions of the
# property (if they are not `None`).
#
# We can't just replace the functions, because `fget`, `fset` and `fdel` are
# actually read-only properties themselves, that return the original functions.
# But we could create a new property based off thge original one, substituting
# our decorated getter, setter and deleter.
#
# Recall that the `getter()`, `setter()` and `deleter()` methods are methods that
# will create a copy of the original property, but substitute the `fget`, `fset`
# and `fdel` methods (that's how these are used as decorators).

# In[48]:


def class_logger(cls):
    for name, obj in vars(cls).items():
        if callable(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))
        elif isinstance(obj, staticmethod):
            original_func = obj.__func__
            print('decorating static method', original_func)
            decorated_func = func_logger(original_func)
            method = staticmethod(decorated_func)
            print(method, type(method))
            setattr(cls, name, method)
        elif isinstance(obj, classmethod):
            original_func = obj.__func__
            print('decorating class method', original_func)
            decorated_func = func_logger(original_func)
            method = classmethod(decorated_func)
            setattr(cls, name, method)
        elif isinstance(obj, property):
            print('decorating property', obj)
            if obj.fget:
                obj = obj.getter(func_logger(obj.fget))
            if obj.fset:
                obj = obj.setter(func_logger(obj.fset))
            if obj.fdel:
                obj = obj.deleter(func_logger(obj.fdel))
            setattr(cls, name, obj)
    return cls


# In[49]:


@class_logger
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


# In[50]:


p = Person('David')


# In[51]:


print(p.name)


# Ha!! Pretty cool...

# Let's make sure it works if we have setters and deleters as well:

# In[52]:


@class_logger
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        print('deleting name...')


# In[53]:


p = Person('David')


# In[54]:


print(p.name)


# In[55]:


p.name = 'Beazley'
print(f"Checking setter name={p.name}")

# In[56]:


del(p.name)


# Success!!
#
# A bit mind-bending, but nonetheless, cool stuff!

# Still, this is not perfect... :(

# We can still run into trouble because not every callable is a function that
# can be decorated:

# In[57]:


@class_logger
class Person:
    class Other:
        def __call__(self):
            print('called instance of Other...')

    other = Other()


# So, as you see it decorated both the class `Other` (since classes are
# callables), and it decorated `other` since we made instances of `Other`
# callable too.
#
# How does that work with the logger though:

# In[58]:


print(Person.Other)


# In[59]:


print(Person.other)


# And that's the problem, because `Other` and `other` are callables, they have
# been replaced in our class by what comes out of the decorator - a function.

# So maybe we can use the `inspect` module to restrict our callables further:

# In[60]:


# In[61]:


class MyClass:
    @staticmethod
    def static_method():
        pass

    @classmethod
    def cls_method(cls):
        pass

    def inst_method(self):
        pass

    @property
    def name(self):
        pass

    def __add__(self, other):
        pass

    class Other:
        def __call__(self):
            pass

    other = Other()


# In[62]:

keys = ('static_method', 'cls_method', 'inst_method', 'name', '__add__', 'Other', 'other')
inspect_funcs = ('isroutine', 'ismethod', 'isfunction', 'isbuiltin', 'ismethoddescriptor')


# In[63]:


print(keys)


# In[64]:


max_header_length = max(len(key) for key in keys)
max_fname_length = max(len(func) for func in inspect_funcs)
print(format('', f'{max_fname_length}s'), '\t'.join(
    format(key, f'{max_header_length}s') for key in keys))
for inspect_func in inspect_funcs:
    fn = getattr(inspect, inspect_func)
    inspect_results = (
        format(str(fn(MyClass.__dict__[key])), f'{max_header_length}s') for key in keys)
    print(format(inspect_func, f'{max_fname_length}s'), '\t'.join(inspect_results))


# As you can see we could use inspect to only pick things that are routines
# instead of more general callables. Properties, static and class methods we are
# already handling specially, so I'm going to move the callable check last in
# the `if...elif` block so we handle static and class methods first (since they
# are classified as routines too).

# In[65]:


def class_logger(cls):
    for name, obj in vars(cls).items():
        if isinstance(obj, staticmethod):
            original_func = obj.__func__
            print('decorating static method', original_func)
            decorated_func = func_logger(original_func)
            method = staticmethod(decorated_func)
            setattr(cls, name, method)
        elif isinstance(obj, classmethod):
            original_func = obj.__func__
            print('decorating class method', original_func)
            decorated_func = func_logger(original_func)
            method = classmethod(decorated_func)
            setattr(cls, name, method)
        elif isinstance(obj, property):
            print('decorating property', obj)
            if obj.fget:
                obj = obj.getter(func_logger(obj.fget))
            if obj.fset:
                obj = obj.setter(func_logger(obj.fset))
            if obj.fdel:
                obj = obj.deleter(func_logger(obj.fdel))
            setattr(cls, name, obj)
        elif inspect.isroutine(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))
    return cls


# In[66]:


@class_logger
class MyClass:
    @staticmethod
    def static_method():
        print('static_method called...')

    @classmethod
    def cls_method(cls):
        print('class method called...')

    def inst_method(self):
        print('instance method called...')

    @property
    def name(self):
        print('name getter called...')

    def __add__(self, other):
        print('__add__ called...')

    class Other:
        def __call__(self):
            print(f'{self}.__call__ called...')

    other = Other()


# In[67]:

print(MyClass.Other, MyClass.other)


# In[68]:


print(MyClass.other())


# No log, that was expected.

# In[69]:


print(MyClass.static_method())


# In[70]:


print(MyClass.cls_method())


# In[71]:


print(MyClass().inst_method())


# In[72]:


print(MyClass().name)


# In[73]:


print(MyClass() + MyClass())


# If we really wanted to, we could also decorate the `Other` class:

# In[74]:


@class_logger
class MyClass:
    @staticmethod
    def static_method():
        print('static_method called...')

    @classmethod
    def cls_method(cls):
        print('class method called...')

    def inst_method(self):
        print('instance method called...')

    @property
    def name(self):
        print('name getter called...')

    def __add__(self, other):
        print('__add__ called...')

    @class_logger
    class Other:
        def __call__(self):
            print(f'{self}.__call__ called...')

    other = Other()


# In[75]:

print(MyClass.other())


# We could also do a bit of DRYing on our decorator code.
#
# First let's handle the static and class methods:

# In[76]:


def class_logger(cls):
    for name, obj in vars(cls).items():
        if isinstance(obj, staticmethod) or isinstance(obj, classmethod):
            type_ = type(obj)
            original_func = obj.__func__
            print(f'decorating {type_.__name__} method', original_func)
            decorated_func = func_logger(original_func)
            method = type_(decorated_func)
            setattr(cls, name, method)
        elif isinstance(obj, property):
            print('decorating property', obj)
            if obj.fget:
                obj = obj.getter(func_logger(obj.fget))
            if obj.fset:
                obj = obj.setter(func_logger(obj.fset))
            if obj.fdel:
                obj = obj.deleter(func_logger(obj.fdel))
            setattr(cls, name, obj)
        elif inspect.isroutine(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))
    return cls


# In[77]:


@class_logger
class MyClass:
    @staticmethod
    def static_method():
        print('static_method called...')

    @classmethod
    def cls_method(cls):
        print('class method called...')

    def inst_method(self):
        print('instance method called...')

    @property
    def name(self):
        print('name getter called...')

    def __add__(self, other):
        print('__add__ called...')

    @class_logger
    class Other:
        def __call__(self):
            print(f'{self}.__call__ called...')

    other = Other()


# In[78]:


print(MyClass.static_method())


# In[79]:


print(MyClass.cls_method())


# Finally, let's see if we can clean up the block to handle properties - I don't
# like these repeated nested if statements that basically do the almost same thing:

# In[80]:


def class_logger(cls):
    for name, obj in vars(cls).items():
        if isinstance(obj, staticmethod) or isinstance(obj, classmethod):
            type_ = type(obj)
            original_func = obj.__func__
            print(f'decorating {type_.__name__} method', original_func)
            decorated_func = func_logger(original_func)
            method = type_(decorated_func)
            setattr(cls, name, method)
        elif isinstance(obj, property):
            print('decorating property', obj)
            methods = (('fget', 'getter'), ('fset', 'setter'), ('fdel', 'deleter'))
            for prop, method in methods:
                if getattr(obj, prop):
                    obj = getattr(obj, method)(func_logger(getattr(obj, prop)))
            setattr(cls, name, obj)
        elif inspect.isroutine(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))
    return cls


# In[81]:


@class_logger
class MyClass:
    @staticmethod
    def static_method():
        print('static_method called...')

    @classmethod
    def cls_method(cls):
        print('class method called...')

    def inst_method(self):
        print('instance method called...')

    @property
    def name(self):
        print('name getter called...')

    @name.setter
    def name(self, value):
        print('name setter called...')

    @name.deleter
    def name(self):
        print('name deleter called...')

    def __add__(self, other):
        print('__add__ called...')

    @class_logger
    class Other:
        def __call__(self):
            print(f'{self}.__call__ called...')

    other = Other()


# In[82]:


print(MyClass().name)


# In[83]:


MyClass().name = 'David'
print(f"Checking setter name={p.name}")


# In[84]:


del MyClass().name


# In[ ]:




