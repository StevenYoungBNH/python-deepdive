#!/usr/bin/env python
# coding: utf-8

# ### Custom Classes

# We'll cover classes in a lot of detail in this course, but for now you should have at least some understanding of classes in Python and how to create them.

# To create a custom class we use the `class` keyword, and we can initialize class attributes in the special method `__init__`.

# In[1]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# We create **instances** of the `Rectangle` class by calling it with arguments that are passed to the `__init__` method as the second and third arguments. The first argument (`self`) is automatically filled in by Python and contains the object being created.
# 
# Note that using `self` is just a convention (although a good one, and you shgoudl use it to make your code more understandable by others), you could really call it whatever (valid) name you choose.
# 
# But just because you can does not mean you should!

# In[2]:


r1 = Rectangle(10, 20)
r2 = Rectangle(3, 5)


# In[3]:


r1.width


# In[4]:


r2.height


# `width` and `height` are attributes of the `Rectangle` class. But since they are just values (not callables), we call them **properties**.
# 
# Attributes that are callables are called **methods**.

# You'll note that we were able to retrieve the `width` and `height` attributes (properties) using a dot notation, where we specify the object we are interested in, then a dot, then the attribute we are interested in.

# We can add callable attributes to our class (methods), that will also be referenced using the dot notation.
# 
# Again, we will create instance methods, which means the method will require the first argument to be the object being used when the method is called.

# In[5]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(the_referenced_object):
        return 2 * (the_referenced_object.width + the_referenced_object.height)


# In[6]:


r1 = Rectangle(10, 20)


# In[7]:


r1.area()


# When we ran the above line of code, our object was `r1`, so when `area` was called, Python in fact called the method `area` in the Rectangle class automatically passing `r1` to the `self` parameter.

# This is why we can use a name other than self, such as in the perimeter method:

# In[8]:


r1.perimeter()


# Again, I'm just illustrating a point, don't actually do that!

# In[9]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


# In[10]:


r1 = Rectangle(10, 20)


# Python defines a bunch of **special** methods that we can use to give our classes functionality that resembles functionality of built-in and standard library objects.
# 
# Many people refer to them as *magic* methods, but there's nothing magical about them - unlike magic, they are well documented and understood!!
# 
# These **special** methods provide us an easy way to overload operators in Python.

# For example, we can obtain the string representation of an integer using the built-in `str` function:

# In[11]:


str(10)


# What happens if we try this with our Rectangle object?

# In[12]:


str(r1)


# Not exactly what we might have expected. On the other hand, how is Python supposed to know how to display our rectangle as a string?
# 
# We could write a method in the class such as:

# In[13]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def to_str(self):
        return 'Rectangle (width={0}, height={1})'.format(self.width, self.height)


# So now we could get a string from our object as follows:

# In[14]:


r1 = Rectangle(10, 20)
r1.to_str()


# But of course, using the built-in `str` function still does not work:

# In[15]:


str(r1)


# Does this mean we are out of luck, and anyone who writes a class in Python will need to provide some method to do this, and probably come up with their own name for the method too, maybe `to_str`, `make_string`, `stringify`, and who knows what else.

# Fortunately, this is where these special methods come in. When we call `str(r1)`, Python will first look to see if our class (`Rectangle`) has a special method called `__str__`.
# 
# If the `__str__` method is present, then Python will call it and return that value.
# 
# There's actually another one called `__repr__` which is related, but we'll just focus on `__str__` for now.

# In[16]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return 'Rectangle (width={0}, height={1})'.format(self.width, self.height)


# In[17]:


r1 = Rectangle(10, 20)


# In[18]:


str(r1)


# However, in Jupyter (and interactive console if you are using that), look what happens here:

# In[19]:


r1


# As you can see we still get that default. That's because here Python is not converting `r1` to a string, but instead looking for a string *representation* of the object. It is looking for the `__repr__` method (which we'll come back to later).

# In[20]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return 'Rectangle (width={0}, height={1})'.format(self.width, self.height)
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)


# In[21]:


r1 = Rectangle(10, 20)


# In[22]:


print(r1)  # uses __str__


# In[23]:


r1  # uses __repr__


# How about the comparison operators, such as `==` or `<`?

# In[24]:


r1 = Rectangle(10, 20)
r2 = Rectangle(10, 20)


# In[25]:


r1 == r2


# As you can see, Python does not consider `r1` and `r2` as equal (using the `==` operator). Again, how is Python supposed to know that two Rectangle objects with the same height and width should be considered equal?

# We just need to tell Python how to do it, using the special method `__eq__`.

# In[40]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return 'Rectangle (width={0}, height={1})'.format(self.width, self.height)
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)
    
    def __eq__(self, other):
        print('self={0}, other={1}'.format(self, other))
        if isinstance(other, Rectangle):
            return (self.width, self.height) == (other.width, other.height)
        else:
            return False


# In[41]:


r1 = Rectangle(10, 20)
r2 = Rectangle(10, 20)


# In[42]:


r1 is r2


# In[43]:


r1 == r2


# In[44]:


r3 = Rectangle(2, 3)


# In[45]:


r1 == r3


# And if we try to compare our Rectangle to a different type:

# In[46]:


r1 == 100


# Let's remove that print statement - I only put that in so you could see what the arguments were, in practice you should avoid side effects.

# In[47]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return 'Rectangle (width={0}, height={1})'.format(self.width, self.height)
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)
    
    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return (self.width, self.height) == (other.width, other.height)
        else:
            return False


# What about `<`, `>`, `<=`, etc.?
# 
# Again, Python has special methods we can use to provide that functionality.
# 
# These are methods such as `__lt__`, `__gt__`, `__le__`, etc.

# In[48]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return 'Rectangle (width={0}, height={1})'.format(self.width, self.height)
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)
    
    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return (self.width, self.height) == (other.width, other.height)
        else:
            return False
    
    def __lt__(self, other):
        if isinstance(other, Rectangle):
            return self.area() < other.area()
        else:
            return NotImplemented


# In[49]:


r1 = Rectangle(100, 200)
r2 = Rectangle(10, 20)


# In[50]:


r1 < r2


# In[51]:


r2 < r1


# What about `>`?

# In[52]:


r1 > r2


# How did that work? We did not define a `__gt__` method.
# 
# Well, Python cleverly decided that since `r1 > r2` was not implemented, it would give 
# 
# `r2 < r1` 
# 
# a try. And since, `__lt__` **is** defined, it worked!

# Of course, `<=` is not going to magically work!

# In[53]:


r1 <= r2


# If you come from a Java background, you are probably thinking that using "bare" properties (direct access), such as `height` and `width` is a terrible design idea.
# 
# It is for Java, but not for Python.
# 
# Although you can use bare properties in Java, if you ever need to intercept the getting or setting of a property, you will need to write a method (such as `getWidth` and `setWidth`. The problem is that if you used a bare `width` property for example, a lot of your code might be using `obj.width` (as we have been doing here). The instant you make the `width` private and instead implement getters and setters, you break your code.
# Hence one of the reasons why in Java we just write getters and setters for properties from the beginning.
# 
# With Python this is not the case - we can change any bare property into getters and setters without breaking the code that uses that bare property.
# 
# I'll show you a quick example here, but we'll come back to this topic in much more detail later.

# Let's take our Rectangle class once again. I'll use a simplified version to keep the code short.

# In[54]:


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)


# In[55]:


r1 = Rectangle(10, 20)


# In[56]:


r1.width


# In[57]:


r1.width = 100


# In[58]:


r1


# As you saw we can *get* and *set* the `width` property directly.
# 
# But let's say after this code has been released for a while and users of our class have been using it (and specifically setting and getting the `width` and `height` attribute a lot), but now we want to make sure users cannot set a non-positive value (i.e. <= 0) for width (or height, but we'll focus on width as an example).

# In a language like Java, we would implement `getWidth` and `setWidth` and make `width` private - which would break any code directly accessing the `width` property.

# In Python we can use some special **decorators** (more on those later) to encapsulate our property getters and setters:

# In[59]:


class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        if width <= 0:
            raise ValueError('Width must be positive.')
        self._width = width
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        if height <= 0:
            raise ValueError('Height must be positive.')
        self._height = height


# In[60]:


r1 = Rectangle(10, 20)


# In[61]:


r1.width


# In[62]:


r1.width = 100


# In[63]:


r1


# In[64]:


r1.width = -10


# There are more things we should do to properly implement all this, in particular we should also be checking the positive and negative values during the `__init__` phase. We do so by using the accessor methods for height and width:

# In[65]:


class Rectangle:
    def __init__(self, width, height):
        self._width = None
        self._height = None
        # now we call our accessor methods to set the width and height
        self.width = width
        self.height = height
    
    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.width, self.height)
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        if width <= 0:
            raise ValueError('Width must be positive.')
        self._width = width
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        if height <= 0:
            raise ValueError('Height must be positive.')
        self._height = height


# In[66]:


r1 = Rectangle(0, 10)


# There more we should be doing, like checking that the width and height being passed in are numeric types, and so on. Especially during the `__init__` phase - we would rather raise an exception when the object is being created rather than delay things and raise an exception when the user calls some method like `area` - that way the exception will be on the line that creates the object - makes debugging much easier!

# There are many more of these special methods, and we'll look in detail at them later in this course.
