#!/usr/bin/env python
# coding: utf-8

# ### Metaclasses vs Class Decorators

# As we have seen, class decorators can achieve a lot of the metaprogramming goals we might have.

# But there is one area where they fall short of metaclasses - inheritance.

# Metaclasses are carried through inheritance, whereas decorators are not.

# Let's go back to the previous class decorator example we had (and I'll use the original one to keep the code simple):

# In[1]:


from functools import wraps

import types


# S. Youngs solution
#def func_logger(fn):
    #@wraps(fn)
    #def inner(*args, **kwargs):
        #try:
            #result = fn(*args, **kwargs)
            #print(f'log: {fn.__qualname__}({args}, {kwargs}) = {result}')
        #except AttributeError as ex:
            #print(f'Log: Function:{fn} Exception: {AttributeError}{ex}')
        #return result
    #return inner

# Fred Baptiste's solution
# https://www.udemy.com/course/python-3-deep-dive-part-4/learn/lecture/16786044#questions/18903900
# This is a more elegant solution than the my version. 
def func_logger(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        result = fn(*args, **kwargs)
        fn_name = getattr(fn, "__qualname__", None) #  static methods don't have a __qualname__
        if not fn_name:
            fn_name = fn.__wrapped__.__qualname__
        print(f'log: {fn_name}({args}, {kwargs}) = {result}')
        return result
    return inner    

def class_logger(cls):
    for name, obj in vars(cls).items():
        if callable(obj):
            print('decorating:', cls, name)
            setattr(cls, name, func_logger(obj))
    return cls


# And as we saw, we can decorate a class with it:

# In[2]:


@class_logger
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f'Hello, my name is {self.name} and I am {self.age}'


# In[3]:


Person('Alex', 10).greet()


# We could do this with a metaclass too:

# In[4]:


class ClassLogger(type):
    def __new__(mcls, name, bases, class_dict):
        new_cls = super().__new__(mcls, name, bases, class_dict)
        for key, obj in vars(new_cls).items():
            if callable(obj):
                # Added this check since __new__ is a builtin type and not a
                # function, therefore it does not have a qualified name when
                # function logger is called. 
                setattr(new_cls, key, func_logger(obj))
        return new_cls        


# In[5]:


class Person(metaclass=ClassLogger):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f'Hello, my name is {self.name} and I am {self.age}'


# In[6]:


p = Person('John', 78).greet()


# So, why not just use a class decorator?

# Now let's see how inheritance works with both those methods.

# Let's do the decorator approach first:

# In[7]:


@class_logger
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f'Hello, my name is {self.name} and I am {self.age}'


# Now let's inherit `Person`:

# In[8]:


class Student(Person):
    def __init__(self, name, age, student_number):
        super().__init__(name, age)
        self.student_number = student_number
        
    def study(self):
        return f'{self.name} studies...'


# In[9]:


s = Student('Alex', 19, 'abcdefg')


# So first off, you can see that the print worked, but only for the `__init__` in the `Person` class, no logs were generated for the `__init__` in the `Student` class.

# By the same token, we don't get logging on the `study` method:

# In[10]:


s.study()


# So we would need to remember to decorate the `Student` class as well:

# In[11]:


@class_logger
class Student(Person):
    def __init__(self, name, age, student_number):
        super().__init__(name, age)
        self.student_number = student_number
        
    def study(self):
        return f'{self.name} studies...'


# In[12]:


s = Student('Alex', 19, 'abcdefg')


# In[13]:


s.greet()


# In[14]:


s.study()


# So, we just have to remember to decorate **every** subclass as well.

# But if we use a metaclass, watch what happens when inherit:

# In[15]:


class Person(metaclass=ClassLogger):
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f'Hello, my name is {self.name} and I am {self.age}'
    
class Student(Person):
    def __init__(self, name, age, student_number):
        super().__init__(name, age)
        self.student_number = student_number
        
    def study(self):
        return f'{self.name} studies...'


# In[16]:


s = Student('Alex', 19, 'abcdefg')


# In[17]:


s.study()


# This works because `Student` inherits from `Person`, and since `Person` uses a 
# metaclass for the creation, this follows down to the `Student` class as well.

# In[18]:


print(type(Person))


# In[19]:


print(type(Student))


# As you can see the type of both the parent and the subclass is `ClassLogger` 
# even though we did not explicitly state that `Student` should use the metaclass
# for creation.
# 
# It happened automatically because we did not have a `__new__` method in the 
# `Student` class, so the parent's `__new__` was essentially used, and that one 
# uses the metaclass.

# We can see this more explicitly this way:

# In[20]:


class Student(Person):
    def __new__(cls, name, age, student_number):
        return super().__new__(cls)
    
    def __init__(self, name, age, student_number):
        super().__init__(name, age)
        self.student_number = student_number
        
    def study(self):
        return f'{self.name} studies...'


# In[21]:


s = Student('Alex', 19, 'ABC')


# In[22]:


s.study()


# One of the disadvantages of metaclasses vs class decorators is that only a
# "single" metaclass can be used. (Actually it's a bit more subtle than that, we
# can use a different metaclass in for a subclass if the metclass is a subclass
# of the parent's metaclass - we'll cover this point again when we look at 
# multiple inheritance.)

# In[26]:


class Metaclass1(type):
    pass

class Metaclass2(type):
    pass


# In[27]:


# class Person(metaclass=Metaclass1):
    pass


# In[28]:


# class Student(Person, metaclass=Metaclass2):
    pass


# As you can see we cannot specify a custom metaclass for `Student` because that would conflict with the class it is inheriting from.

# An exception is if we inherit from a parent who has `type` as its metaclass:

# In[29]:


class Person:
    pass

class Student(Person, metaclass=Metaclass1):
    pass


# In[30]:


p = Person()
s = Student()


# In[31]:


type(Person), type(Student)


# It can also cause problems in multiple inheritance.
# 
# We haven't covered multiple inheritance yet, but let me show you the issue at least:

# In[32]:


class Class1(metaclass=Metaclass1):
    pass

class Class2(metaclass=Metaclass2):
    pass


# Here we have created two classes that use different custom metaclasses.
# 
# If we try to create a new class that inherits from both:

# In[33]:


#class MultiClass(Class1, Class2):
#    pass


# Again, if one of the base classes is `type` and the other is a custom metaclass, then this is allowed (this is because `Metaclass1` is itself a subclass of `type`:

# In[36]:


class Class1(metaclass=type):
    pass

class Class2(metaclass=Metaclass1):
    pass


# In[37]:


class MultiClass(Class1, Class2):
    pass


# On the other hand we can stack decorators as much as we want (we just have to be careful with the order in which we stack them sometimes).
