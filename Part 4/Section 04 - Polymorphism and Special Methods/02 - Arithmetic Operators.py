#!/usr/bin/env python
# coding: utf-8

# ### Arithmetic Operators

# Let's first look at some simple example of using the straightforward `__add__`, `__sub__`, etc.

# Let's say we want to implement a `Vector` class that supports various arithmetic operations. We won't assume a specific number of dimensions - that will be determined by how many arguments are passed to the `__init__` method. We will however require the arguments to be Real numbers.
# 

# In[1]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'


# Now, let's support addition and subtraction of vectors - they'll need to be of the same dimension, othwerwise we should raise a `TypeError` exception (consistent with the exception Python raises if you try to add a string and an int for example).

# In[2]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)


# Let's try out our class and see how things work at this point:

# In[3]:


v1 = Vector(1, 2)
v2 = Vector(10, 10)
v3 = Vector(1, 2, 3, 4)


# In[4]:


v1


# In[5]:


v1 + v2


# In[6]:


v2 + v1 


# In[7]:


try:
    print(v1 + v3)
except TypeError as ex:
    print(ex)


# In[8]:


try:
    print(v1 + 100)
except TypeError as ex:
    print(ex)


# Now, let's add support for multiplication by a scalar value - e.g. multipliying a vector by a real num ber (not another vector).
# 
# To do that we'll implement the `__mul__` method:

# In[9]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if not isinstance(other, Real):
            return NotImplemented
        components = (other * x for x in self.components)
        return Vector(*components)


# In[10]:


v1 = Vector(1, 2)


# In[11]:


v1 * 10


# But what happens if we reverse the operation:

# In[12]:


try:
    10 * v1
except TypeError as ex:
    print(ex)


# What happened here is that Python first tried calling the addition operation on the `int` object, using the `Vector` as the second operand. Integers of course do no support this type, so Python tried using our `Vector` class - but not the `__mul__` since that is called when the `Vector` is the **left** operand. Instead, it is looking for (and does not find) a method to use when the `Vector` is the **right** operand.
# 
# We can implement this method, using `__rmul__`:

# In[13]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if not isinstance(other, Real):
            return NotImplemented
        components = (other * x for x in self.components)
        return Vector(*components)
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other


# In[14]:


v1 = Vector(1, 2)


# In[15]:


v1 * 10


# In[16]:


10 * v1


# Now, let's say we want to implement the dot product of two vectors.
# 
# If you are rusty on this, just do a quick read of this: https://en.wikipedia.org/wiki/Dot_product
# 
# Basically we need vectors of equal dimension, and we calculate the sum of the product of components (pairwise) in each vector.
# 
# We can implement it by differentiating between a `Real` and ` Vector` type in our `__mul__` method - of course we won't need it in the `__rmul__` method because if we implement multiplication between two `Vectors` we'll always have a `Vector` as the left operand, so `__mul__` will get called first.

# In[17]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if isinstance(other, Real):
            components = (other * x for x in self.components)
            return Vector(*components)
        if self.validate_type_and_dimension(other):
            # dot product
            components = (x * y for x, y in zip(self.components, other.components))
            return sum(components)
        return NotImplemented
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other


# In[18]:


v1 = Vector(1, 2)
v2 = Vector(3, 4)


# In[19]:


v1 * v2


# We could also implement the **cross** product of two vectors (which would return another vector).
# 
# The calculations get a little more complicated, so I won't show you those details, but let's see how we could use the `@` operator to implement this:

# In[20]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if isinstance(other, Real):
            components = (other * x for x in self.components)
            return Vector(*components)
        if self.validate_type_and_dimension(other):
            # dot product
            components = (x * y for x, y in zip(self.components, other.components))
            return sum(components)
        return NotImplemented
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
    
    def __matmul__(self, other):
        print('__matmul__ called...')


# In[21]:


v1 = Vector(1, 2)
v2 = Vector(3, 4)


# In[22]:


v1 * v2


# In[23]:


v1 @ v2


# #### In-Place Operators

# We also have the in-place operators. Typically in-place operators will try to **mutate** the object on the left of the expression:

# In[24]:


l = [1, 2]


# In[25]:


id(l)


# In[26]:


l += [3]


# In[27]:


id(l), l


# As you can see, the list `l` mas mutated (memory address remained the same). This is not the same effect as:

# In[28]:


l = [1, 2]
print(id(l))

l = l + [3]
print(id(l), l)


# As you can see, here we ended up with a **new** list object.
# 
# But in-place does **not** *guarantee* a mutation. For example, tuples are immutable objects:

# In[29]:


t = (1, 2)
print(id(t))
t += (3, )
print(id(t), t)


# As you can see we ended up with a new tuple. Same thing happens with strings, integers, floats and so on, that are also immutable types. 

# Let's go back to our `Vector` class and implement in-place addition - but we'll implement it in such a way that we do not mutate the Vector, instead just returning a new Vector - similar to what we just saw with tuples:

# In[30]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if isinstance(other, Real):
            components = (other * x for x in self.components)
            return Vector(*components)
        if self.validate_type_and_dimension(other):
            # dot product
            components = (x * y for x, y in zip(self.components, other.components))
            return sum(components)
        return NotImplemented
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
    
    def __iadd__(self, other):
        print('__radd__ called...')
        return self + other


# In[31]:


v1 = Vector(1, 2)
v2 = Vector(10, 10)

print(id(v1))

v1 += v2

print(id(v1), v1)


# As you can see, we end up with a new `Vector` object.
# 
# Now let's modify this so we actually mutate the `Vector` object:

# In[32]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if isinstance(other, Real):
            components = (other * x for x in self.components)
            return Vector(*components)
        if self.validate_type_and_dimension(other):
            # dot product
            components = (x * y for x, y in zip(self.components, other.components))
            return sum(components)
        return NotImplemented
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
    
    def __iadd__(self, other):
        print('__radd__ called...')
        if self.validate_type_and_dimension(other):
            components = (x + y for x, y in zip(self.components, other.components))
            self._components = tuple(components)  # mutating our Vector object
            return self # don't forget to return the result of the operation!
        return NotImplemented
        


# In[33]:


v1 = Vector(1, 2)
v2 = Vector(10, 20)

print(id(v1))

v1 += v2

print(id(v1), v1)


# As you can see we **mutated** the object `v1`.

# Let's also implement the unary minus on our `Vector` class. In this case we just want to return a new `Vector` with each component negated:

# In[34]:


from numbers import Real

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if isinstance(other, Real):
            components = (other * x for x in self.components)
            return Vector(*components)
        if self.validate_type_and_dimension(other):
            # dot product
            components = (x * y for x, y in zip(self.components, other.components))
            return sum(components)
        return NotImplemented
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
    
    def __iadd__(self, other):
        print('__radd__ called...')
        if self.validate_type_and_dimension(other):
            components = (x + y for x, y in zip(self.components, other.components))
            self._components = tuple(components)  # mutating our Vector object
            return self # don't forget to return the result of the operation!
        return NotImplemented
        
    def __neg__(self):
        print('__neg__ called...')
        components = (-x for x in self.components)
        return Vector(*components)


# In[35]:


v1 = Vector(1, 2)
-v1


# So we can use it in arithmetic operations such as:

# In[36]:


v2 = Vector(10, 10)

v2 + -v1


# Lastly, let's implement the `abs` function for our Vector. Right now it won't work:

# In[37]:


try:
    abs(v1)
except TypeError as ex:
    print(ex)


# But we can fix that:

# In[38]:


from numbers import Real
from math import sqrt

class Vector:
    def __init__(self, *components):
        # validate number of components is at least one, and all of them are real numbers
        if len(components) < 1:
            raise ValueError('Cannot create an empty Vector.')
        for component in components:
            if not isinstance(component, Real):
                raise ValueError(f'Vector components must all be real numbers - {component} is invalid.')
        
        # use immutable storage for vector
        self._components = tuple(components)
        
    def __len__(self):
        return len(self._components)
        
    @property
    def components(self):
        return self._components
    
    def __repr__(self):
        # works - but unwieldy for high dimension vectors
        return f'Vector{self._components}'
    
    def validate_type_and_dimension(self, v):
        return isinstance(v, Vector) and len(v) == len(self)
            
    def __add__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x + y for x, y in zip(self.components, other.components))
        return Vector(*components)
            
    def __sub__(self, other):
        if not self.validate_type_and_dimension(other):
            return NotImplemented
        components = (x - y for x, y in zip(self.components, other.components))
        return Vector(*components)
    
    def __mul__(self, other):
        print('__mul__ called...')
        if isinstance(other, Real):
            components = (other * x for x in self.components)
            return Vector(*components)
        if self.validate_type_and_dimension(other):
            # dot product
            components = (x * y for x, y in zip(self.components, other.components))
            return sum(components)
        return NotImplemented
    
    def __rmul__(self, other):
        print('__rmul__ called...')
        # for us, multiplication is commutative, so we can leverage our existing __mul__ method
        return self * other
    
    def __iadd__(self, other):
        print('__radd__ called...')
        if self.validate_type_and_dimension(other):
            components = (x + y for x, y in zip(self.components, other.components))
            self._components = tuple(components)  # mutating our Vector object
            return self # don't forget to return the result of the operation!
        return NotImplemented
        
    def __neg__(self):
        print('__neg__ called...')
        components = (-x for x in self.components)
        return Vector(*components)
    
    def __abs__(self):
        print('__abs__ called...')
        return sqrt(sum(x ** 2 for x in self.components))


# In[39]:


v1 = Vector(1, 1)


# In[40]:


abs(v1)


# #### Other Uses

# Of course, these arithmetic operators are not restricted to working with numbers. We've seen them work with strings as well for example, or lists even.
# 
# We can also use them in our custom classes in different ways where we want to implement and attach special meaning to these operators.
# 
# For example, we might have a `Family` class that holds together:
# - mother and father `Person` objects
# - a list of children `Person` objects
# 
# We want to make it such that we can add children simply by using inplace addition.

# In[41]:


class Person:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f"Person('{self.name}')"


# In[42]:


p1 = Person('John')


# In[43]:


class Family:
    def __init__(self, mother, father):
        self.mother = mother
        self.father = father
        self.children = []
        
    def __iadd__(self, other):
        self.children.append(other)
        return self
    


# In[44]:


f = Family(Person('Mary'), Person('John'))
print(id(f))


# In[45]:


f += Person('Eric')
print(id(f))
print(f.children)


# In[46]:


f += Person('Michael')
print(id(f))
print(f.children)


# So, don't feel restricted to using these operators for numerical use cases only.
