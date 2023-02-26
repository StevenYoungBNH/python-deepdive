#!/usr/bin/env python
# coding: utf-8

# ### Customizing and Extending Enumerations

# Enumerations, although they behave a little differently than normal classes, are **still** classes.

# This means there are many things we can customize about them.

# Keep in mind that members of the enumerations are **instances** of the enumeration class, so we can implement methods in that class, and each member will have that method (boud to itself) available.

# In[1]:


from enum import Enum


# In[2]:


class Color(Enum):
    red = 1
    green = 2
    blue = 3
    
    def purecolor(self, value):
        return {self: value}


# In[3]:


Color.red.purecolor(100), Color.blue.purecolor(200)


# Amongst other things, we can implement some of the "standard" dunder methods. For example we may wish to override the default representation:

# In[4]:


Color.red


# In[5]:


class Color(Enum):
    red = 1
    green = 2
    blue = 3
    
    def __repr__(self):
        return f'{self.name} ({self.value})'


# In[6]:


Color.red


# Of course, we can implement other more interesting dunder methods.

# For example, in standard enums, we do not have ordering defined for the members:

# In[7]:


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


# In[8]:


try:
    Number.ONE > Number.TWO
except TypeError as ex:
    print(ex)


# But in this particular example it might make sense to actually have ordering defined. We can simply implement some of the rich comparison operators:

# In[9]:


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    
    def __lt__(self, other):
        return isinstance(other, Number) and self.value < other.value


# And now we have an ordering defined:

# In[10]:


Number.ONE < Number.TWO


# In[11]:


Number.TWO > Number.ONE


# We could also potentially override the definition for equality (`==`):

# In[12]:


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    
    def __lt__(self, other):
        return isinstance(other, Number) and self.value < other.value
    
    def __eq__(self, other):
        if isinstance(other, Number):
            return self is other
        elif isinstance(other, int):
            return self.value == other
        else:
            return False


# In[13]:


Number.ONE == Number.ONE


# In[14]:


Number.ONE == 1.0


# In[15]:


Number.ONE == 1


# A good question to ask ourselves is whether our members are still hashable since we implemented a custom `__eq__` method:

# In[16]:


try:
    hash(Number.ONE)
except TypeError as ex:
    print(ex)


# And of course, they are not. We could remedy this by implementing our own `__hash__` method.

# Going back to ordering:

# In[17]:


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    
    def __lt__(self, other):
        return isinstance(other, Number) and self.value < other.value


# Although we have `<` (and by reflection `>`) defined, we still do not have operators such as `<=`:

# In[18]:


try:
    Number.ONE <= Number.TWO
except TypeError as ex:
    print(ex)


# We could of course define a `__le__` method, but we could also just use the `@totalordering` decorator:

# In[19]:


from functools import total_ordering


# In[20]:


@total_ordering
class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    
    def __lt__(self, other):
        return isinstance(other, Number) and self.value < other.value


# In[21]:


Number.ONE <= Number.TWO, Number.ONE != Number.TWO


# A slightly more useful application of this ability to implement these special methods might be in this example:

# In[22]:


class Phase(Enum):
    READY = 'ready'
    RUNNING = 'running'
    FINISHED = 'finished'
    
    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Phase):
            return self is other
        elif isinstance(other, str):
            return self.value == other
        return False
    
    def __lt__(self, other):
        ordered_items = list(Phase)
        self_order_index = ordered_items.index(self)
        
        if isinstance(other, Phase):
            other_order_index = ordered_items.index(other)
            return self_order_index < other_order_index
        
        if isinstance(other, str):
            try:
                other_member = Phase(other)
                other_order_index = ordered_items.index(other_member)
                return self_order_index < other_order_index
            except ValueError:
                # other is not a value in our enum
                return False
            


# In[23]:


Phase.READY == 'ready'


# In[24]:


Phase.READY < Phase.RUNNING


# In[25]:


Phase.READY < 'running'


# One thing to watch out for, is that, by default, all members of an enumeration are **truthy** - irrespective of their value:

# In[26]:


class State(Enum):
    READY = 1
    BUSY = 0    


# In[27]:


bool(State.READY), bool(State.BUSY)


# We can of course override the `__bool__` method to customize this:

# In[28]:


class State(Enum):
    READY = 1
    BUSY = 0    
    
    def __bool__(self):
        return bool(self.value)


# In[29]:


bool(State.READY), bool(State.BUSY)


# So we might implement this ready/not-ready flag in our application by simply testing the truthyness of the member:

# In[30]:


request_state = State.READY


# In[31]:


if request_state:
    print('Launching next query')
else:
    print('Not ready for another query yet')


# We could also easily implement a default associated truth value that reflects the truthyness of the member **values**:

# In[32]:


class Dummy(Enum):
    A = 0
    B = 1
    C = ''
    D = 'python'
    
    def __bool__(self):
        return bool(self.value)


# In[33]:


bool(Dummy.A), bool(Dummy.B), bool(Dummy.C), bool(Dummy.D)


# #### Extending Custom Enumerations

# We can also extend (subclass) our custom enumerations - but only under certain circumstances: as long as the enumeration we are extending does not define any **members**:

# In[34]:


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


# In[35]:


try:
    class ColorAlpha(Color):
        ALPHA = 4
except TypeError as ex:
    print(ex)


# But this would work:

# In[36]:


class ColorBase(Enum):
    def hello(self):
        return f'{str(self)} says hello!'
    
class Color(ColorBase):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


# In[37]:


Color.RED.hello()


# This might not seem particularly useful (we cannot use subclassing to extended the members), but remember that we can add methods to our enumerations - this means we could define a base class that implements some common functionality for all our instances, and then extend this enumeration class to concrete enumerations that define the members.

# Here's an example of where this might be useful:

# In[38]:


@total_ordering
class OrderedEnum(Enum):
    """Creates an ordering based on the member values. 
    So member values have to support rich comparisons.
    """
    
    def __lt__(self, other):
        if isinstance(other, OrderedEnum):
            return self.value < other.value
        return NotImplemented


# And now we can create other enumerations that will support ordering without having to retype the `__lt__` implementation, or even the decorator:

# In[39]:


class Number(OrderedEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    
class Dimension(OrderedEnum):
    D1 = 1,
    D2 = 1, 1
    D3 = 1, 1, 1


# In[40]:


Number.ONE < Number.THREE


# In[41]:


Dimension.D1 < Dimension.D3


# In[42]:


Number.ONE >= Number.ONE


# In[43]:


Dimension.D1 >= Dimension.D2


# Of course we could implement other functionality in our base enum (maybe customized `__str__`, `__repr__`, `__bool__`, etc).

# We'll actually come back to this when we discuss auto numbering in enums.

# #### Example

# Here's a handy enumeration that's built-in to Python (handy if you work with http requests that is :-) )

# In[44]:


from http import HTTPStatus


# In[45]:


type(HTTPStatus)


# It's technically an `EnumMeta`, but that's beyond our current scope. Still, it's easy to use and you don't need to know anything about meta classes:

# In[46]:


list(HTTPStatus)[0:10]


# In[47]:


HTTPStatus(200)


# In[48]:


HTTPStatus.OK, HTTPStatus.OK.name, HTTPStatus.OK.value


# In[49]:


HTTPStatus(200)


# In[50]:


HTTPStatus['OK']


# It even has a `phrase` property that provides a more readable version of the HTTP status (name):

# In[51]:


HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.name, HTTPStatus.NOT_FOUND.phrase


# Now we could implement similar functionality very easily - maybe for our own error codes in our application:

# In[52]:


class AppStatus(Enum):
    OK = (0, 'No problem!')
    FAILED = (1, 'Crap!')


# In[53]:


AppStatus.OK


# In[54]:


AppStatus.OK.value


# What we really want is to separate the code (lie `0`) from the phrase (like `No problem!`). We could do this:

# In[55]:


class AppStatus(Enum):
    OK = (0, 'No problem!')
    FAILED = (1, 'Crap!')
    
    @property
    def code(self):
        return self.value[0]
    
    @property
    def phrase(self):
        return self.value[1]


# In[56]:


AppStatus.OK.code, AppStatus.OK.phrase


# As you can see, it's close, but not quite the same as `HTTPStatus`...
# 
# One major problem is that we can no longer lookup a member by just the code:

# In[57]:


try:
    AppStatus(0)
except ValueError as ex:
    print(ex)


# We would have to do this:

# In[58]:


AppStatus((0, 'No problem!'))


# Not ideal...

# #### Let's dig in...

# OK, so, we can actually fix this issue by making use of the `__new__` method (which we have not studied yet, but I did mention it). 
# 
# Remember that this is the method that gets called to **instantiate** the class - so it should return a new instance of the class. 
# 
# Furthemore we'll have it set the value property - for that `Enum` has a special class attribute we can use, called `_value_`. 
# 
# This is probably going to be a little confusing, but we'll circle back to this later:

# In[59]:


class AppStatus(Enum):
    OK = (0, 'No Problem!')
    FAILED = (1, 'Crap!')
    
    def __new__(cls, member_value, member_phrase):
        # create a new instance of cls
        member = object.__new__(cls)
        
        # set up instance attributes
        member._value_ = member_value
        member.phrase = member_phrase
        return member


# In[60]:


AppStatus.OK.value, AppStatus.OK.name, AppStatus.OK.phrase


# And now even looking up by numeric code works:

# In[61]:


AppStatus(0)


# Now, we could easily break this out into a base class:

# In[62]:


class TwoValueEnum(Enum):
    def __new__(cls, member_value, member_phrase):
        member = object.__new__(cls)
        member._value_ = member_value
        member.phrase = member_phrase
        return member


# And then inherit this for any enumeration where we want to support a value as a `(code, phrase)` tuple:

# In[63]:


class AppStatus(TwoValueEnum):
    OK = (0, 'No Problem!')
    FAILED = (1, 'Crap!')


# In[64]:


AppStatus.FAILED, AppStatus.FAILED.name, AppStatus.FAILED.value, AppStatus.FAILED.phrase


# In[ ]:




