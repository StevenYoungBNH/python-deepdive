#!/usr/bin/env python
# coding: utf-8

# ### Class and Static Methods

# Asd we saw, when we define a function inside a class, how it behaves (as a function or a method) depends on how the function is accessed: from the class, or from the instance. (We'll cover how that works when we look at descriptors later in this course).

# In[1]:


class Person:
    def hello(arg='default'):
        print(f'Hello, with arg={arg}')


# If we call `hello` from the class:

# In[2]:


Person.hello()


# You'll notice that `hello` was called without any arguments, in fact, `hello` is a regular function:

# In[3]:


Person.hello


# But if we call `hello` from an instance, things are different:

# In[4]:


p = Person()


# In[5]:


p.hello


# In[6]:


p.hello()


# In[7]:


hex(id(p))


# And as you can see the instance `p` was passed as an argument to `hello`. 
# 
# Sometimes however, we define functions in a class that do not interact with the instance itself, but may need something from the class. In those cases, we want the class to be passed to the function as an argument, whether it is called from the class or from an instance of the class.
# 
# These are called **class methods**. You'll note that the behavior needs to be different - we don't want the instance to be passed to the function when called from an instance, we want the **class** to be passed to it. In addition, when called from the class, we **also** want the class to be passed to it (this is similar to `static` methods in Java, not to be confused with, as we'll see in a bit, static methods in Python).
# 
# We use the `@classmethod` decorator to define class methods, and the first argument of these methods will always be the class where the method is defined.

# Let's see a simple example first:

# In[8]:


class MyClass:
    def hello():
        # this IS an instance method, we just forgot to add a parameter to capture the instance
        # when this is called from an instance - so this will fail
        print('hello...')
        
    def instance_hello(arg):
        print(f'hello from {arg}')
        
    @classmethod
    def class_hello(arg):
        print(f'hello from {arg}')
        


# In[9]:


m = MyClass()


# In[10]:


MyClass.hello()


# But, as expected, this won't work:

# In[11]:


try:
    m.hello()
except TypeError as ex:
    print(ex)


# On the other hand, notice now the instance method when called from the instance and the class:

# In[12]:


m.instance_hello()


# In[13]:


try:
    MyClass.instance_hello()
except TypeError as ex:
    print(ex)


# As you can see, the instance method needs to be called from the instance. If we call it from the class, no argument is passed to the function, so we end up with an exception.
# 
# This is not the case with class methods - whether we call the method from the class, or the instance, that first argument will always be provided by Python, and will be the class object (not the instance).
# 
# Notice how the bindings are different:

# In[14]:


MyClass.class_hello


# In[15]:


m.class_hello


# As you can see in both these cases, `class_hello` is bound to the class.
# 
# But with an instance method, the bindings behave differently:

# In[16]:


MyClass.instance_hello


# In[17]:


m.instance_hello


# So, whenever we call `class_hello` the method is bound to the **class**, and the first argument is the class:

# In[18]:


MyClass.class_hello()


# In[19]:


m.class_hello()


# Although in this example I used `arg` as the parameter name in our methods, the normal **convention** is to use `self` and `cls` - that way everyone knows what we're talking about!

# We sometimes also want to define functions in a class and always have them be just that - functions, never bound to either the class or the instance, however we call them. Often we do this because we need to utility function that is specific to our class, and we want to keep our class self-contained, or maybe we're writing a library of functions (though modules and packages may be more appropriate for this).

# These are called **static** methods. (So be careful here, Python static methods and Java static methods do not have the same meaning!)

# We can define static methods using the `@staticmethod` decorator:

# In[20]:


class MyClass:
    def instance_hello(self):
        print(f'Instance method bound to {self}')
        
    @classmethod
    def class_hello(cls):
        print(f'Class method bound to {cls}')
        
    @staticmethod
    def static_hello():
        print('Static method not bound to anything')


# In[21]:


m = MyClass()


# In[22]:


m.instance_hello()


# In[23]:


MyClass.class_hello()


# In[24]:


m.class_hello()


# And the static method can be called either from the class or the instance, but is never bound:

# In[25]:


MyClass.static_hello


# In[26]:


m.static_hello


# In[27]:


MyClass.static_hello()


# In[28]:


m.static_hello()


# #### Example

# Let's see a more concrete example of using these different method types.
# 
# We're going to create a `Timer` class that will allow us to get the current time (in both UTC and some timezone), as well as record start/stop times.
# 
# We want to have the same timezone for all instances of our `Timer` class with an easy way to change the timezone for all instances when needed.
# 
# If you need to work with timezones, I recommend you use the `pyrz` 3rd party library. Here, I'll just use the standard library, which is definitely not as easy to use as `pytz`.

# In[29]:


from datetime import datetime, timezone, timedelta

class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)


# So `tz` is a class attribute, and we can set it using a class method `set_timezone` - any instances will share the same `tz` value (unless we override it at the instance level)

# In[30]:


Timer.set_tz(-7, 'MST')


# In[31]:


Timer.tz


# In[32]:


t1 = Timer()
t2 = Timer()


# In[33]:


t1.tz, t2.tz


# In[34]:


Timer.set_tz(-8, 'PST')


# In[35]:


t1.tz, t2.tz


# Next we want a function to return the current UTC time. Obviously this has nothing to do with either the class or the instance, so it is a prime candidate for a static method:

# In[36]:


class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    @staticmethod
    def current_dt_utc():
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)


# In[37]:


Timer.current_dt_utc()


# In[38]:


t = Timer()


# In[39]:


t.current_dt_utc()


# Next we want a method that will return the current time based on the set time zone. Obviously the time zone is a class variable, so we'll need to access that, but we don't need any instance data, so this is a prime candidate for a class method:

# In[40]:


class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    @staticmethod
    def current_dt_utc():
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)
        
    @classmethod
    def current_dt(cls):
        return datetime.now(cls.tz)


# In[41]:


Timer.current_dt_utc(), Timer.current_dt()


# In[42]:


t1 = Timer()
t2 = Timer()


# In[43]:


t1.current_dt_utc(), t1.current_dt()


# In[44]:


t2.current_dt()


# And if we change the time zone (we can do so either via the class or the instance, no difference, since the `set_tz` method is always bound to the class):

# In[45]:


t2.set_tz(-7, 'MST')


# In[46]:


Timer.__dict__


# In[47]:


Timer.current_dt_utc(), Timer.current_dt(), t1.current_dt(), t2.current_dt()


# So far we have not needed any instances to work with this class!
# 
# Now we're going to add functionality to start/stop a timer. Obviously we want this to be instance based, since we want to be able to create multiple timers.

# In[48]:


class TimerError(Exception):
    """A custom exception used for Timer class"""
    # (since """...""" is a statement, we don't need to pass)
    
class Timer:
    tz = timezone.utc  # class variable to store the timezone - default to UTC
    
    def __init__(self):
        # use these instance variables to keep track of start/end times
        self._time_start = None
        self._time_end = None
        
    @staticmethod
    def current_dt_utc():
        """Returns non-naive current UTC"""
        return datetime.now(timezone.utc)
    
    @classmethod
    def set_tz(cls, offset, name):
        cls.tz = timezone(timedelta(hours=offset), name)
        
    @classmethod
    def current_dt(cls):
        return datetime.now(cls.tz)
    
    def start(self):
        # internally we always non-naive UTC
        self._time_start = self.current_dt_utc()
        self._time_end = None
        
    def stop(self):
        if self._time_start is None:
            # cannot stop if timer was not started!
            raise TimerError('Timer must be started before it can be stopped.')
        self._time_end = self.current_dt_utc()
        
    @property
    def start_time(self):
        if self._time_start is None:
            raise TimerError('Timer has not been started.')
        # since tz is a class variable, we can just as easily access it from self
        return self._time_start.astimezone(self.tz)  
        
    @property
    def end_time(self):
        if self._time_end is None:
            raise TimerError('Timer has not been stopped.')
        return self._time_end.astimezone(self.tz)
    
    @property
    def elapsed(self):
        if self._time_start is None:
            raise TimerError('Timer must be started before an elapsed time is available')
            
        if self._time_end is None:
            # timer has not ben stopped, calculate elapsed between start and now
            elapsed_time = self.current_dt_utc() - self._time_start
        else:
            # timer has been stopped, calculate elapsed between start and end
            elapsed_time = self._time_end - self._time_start
            
        return elapsed_time.total_seconds()


# In[49]:


from time import sleep

t1 = Timer()
t1.start()
sleep(2)
t1.stop()
print(f'Start time: {t1.start_time}')
print(f'End time: {t1.end_time}')
print(f'Elapsed: {t1.elapsed} seconds')


# In[50]:


t2 = Timer()
t2.start()
sleep(3)
t2.stop()
print(f'Start time: {t2.start_time}')
print(f'End time: {t2.end_time}')
print(f'Elapsed: {t2.elapsed} seconds')


# So our timer works. Furthermore, we want to use `MST` throughout our application, so we'll set it, and since it's a class level attribute, we only need to change it once:

# In[51]:


Timer.set_tz(-7, 'MST')


# In[52]:


print(f'Start time: {t1.start_time}')
print(f'End time: {t1.end_time}')
print(f'Elapsed: {t1.elapsed} seconds')


# In[53]:


print(f'Start time: {t2.start_time}')
print(f'End time: {t2.end_time}')
print(f'Elapsed: {t2.elapsed} seconds')


# In[ ]:




