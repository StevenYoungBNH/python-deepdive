#!/usr/bin/env python
# coding: utf-8

# ### Custom Classes and Hashing

# We know that in order for an object to be usable as a key in a dictionary, it must be hashable.
# In general Python will not allow mutable types to be hashable. I explained why in previous lectures, but it boils down to key retrieval. 
# 
# To retrieve a key/value from a dictionary, we start with the hash of the key, mod (`%`) the size of the dictionary (allocated, not in-use). From that a sequence of search indices is generated (the probe sequence). Python then follows this probe sequence one by one, comparing the requested key with the key at that index, using `==` comparisons (technically it first compares the hasesh themselves, and f they are equal then also compares the keys). If it finds a key which compares equal then it returns that item, otherwise it continues the probe sequence until it either finds the key or sees an empty slot (which means the key does not exist in the dictionary) and bails out of the search.
# 
# If we allowed the key to change, then even if it had the same hash (and hence the same probe sequence), Python would not find it unless it still compared equal.
# 
# So technically it is not required that the key be immutable, what is required is that the hash and equality of the key does not change!

# Remember the difference between equality (`=`) and identity (`is`):

# In[1]:


t1 = (1, 2, 3)


# In[2]:


t2 = (1, 2, 3)


# In[3]:


t1 is t2


# In[4]:


t1 == t2


# In[5]:


d = {t1: 100}


# In[6]:


d[t1]


# In[7]:


d[t2]


# As you can see, even though `t1` and `t2` are different **objects**, we can still retrieve the element from the dictionary using either one - because they compare **equal** to each other, and, in fact, **have the same hash** as well:

# In[8]:


hash(t1), hash(t2)


# One of the basic premises of hashes is that if two objects compare equal, they must have the same hash.

# What happens when we create custom objects? Are these hashable?
# The answer is yes - but our objects could be mutable, how does Python create a hash for these objects then?
# It uses the memory address (`id`) of the object to compute a hash.
# 
# Also, by default, different instances of a custom class instances will never compare equal, since by default it compares the memory address.

# In[9]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'


# In[10]:


p1 = Person('John', 78)
p2 = Person('John', 78)


# In[11]:


id(p1), id(p2)


# In[12]:


p1 == p2


# In[13]:


hash(p1), hash(p2)


# Because of this default hash calculation, we can actually use custom objects as keys in dictionaries:

# In[14]:


p1 = Person('John', 78)
p2 = Person('Eric', 75)
persons = {p1: 'John object', p2: 'Eric object'}


# In[15]:


for k in persons.keys():
    print(k)


# The problem here is that the **only** way to retrieve John for example, is to request the **original** object as the key (since any other instance, even with the same attribute values would not be equal):

# In[16]:


persons[p1]


# But we cannot retrieve it this way:

# In[17]:


p = Person('John', 78)
print(p, id(p))
print(p1, id(p1))


# As you can see they are not the **same** object, they do not compare equal, and their hash is not the same:

# In[18]:


p == p1, hash(p), hash(p1)


# And so:

# In[19]:


persons.get(p, 'not found')


# This may not be the behavior we want - we might want to be able to retrieve John from the dictionary as long as the contents (or some of the contents) matches - i.e. when do we consider two Person instances **equal**.
# 
# To do this we would start by implementing an `__eq__` method in our class:

# In[20]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        else:
            return False


# In[21]:


p1 = Person('John', 78)
p2 = Person('John', 78)


# In[22]:


p1 == p2


# OK, that's great, so let's put `p1` in a dictionary and see if we can recover it using `p2`, which evaluates to equal to `p1`:

# In[23]:


persons = {p1: 'John p1'}


# Huh? Why is a Person instance suddenly unhashable?

# In[25]:


hash(p1)


# The only thing we changed is we implemented the `__eq__` method. Let's just check:

# In[26]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'


# In[27]:


hash(Person('John', 78))


# In[28]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        else:
            return False


# In[29]:


hash(Person('John', 78))


# Yes, that's the reason... But why?

# Remember what I said earlier, if two objects compare equal (`==`) then their hash should also compare equal.
# 
# `p1` and `p2` are distinct objects, but they now compare equal, and if their hash was based on their `id` they would not have equal hashes!
# 
# When we implement an `__eq__` method on a class, Python will no longer provide a default hash. Instead it automatically indicates that the class is not hashable.
# 
# There is a special method `__hash__` which is used by Python when we call the `hash()` function. If that `__hash__` method **is** `None` then Python considers the object unhashable (note I am not saying the `__hash__` function returns `None`, I am saying it should just **be** `None`)

# In[30]:


hash_func = Person.__hash__
print(hash_func)


# Notice how the __hash__ attribute is `None` - it is not a function that returns `None`.

# In fact, we could have done this explicitly ourselves as well:

# In[31]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        else:
            return False
    
    __hash__ = None


# In[32]:


hash(Person('John', 78))


# In fact we can use this technique to mark a custom class, even if it does not implement an `__eq__` method as unhashable:

# In[33]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    __hash__ = None


# In[34]:


hash(Person('John', 78))


# In this case though, we do want Person instances to be hashable so we can recover Person keys in our dictionary based on whether the objects compare equal or not.
# In this case we simply want to create a hash based on `name` and `age`. Since both of these values are themselves hashable it turns out to be pretty easy to do:

# In[35]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        else:
            return False
    
    def __hash__(self):
        print('__hash__ called...')
        return hash((self.name, self.age))


# In[36]:


p1 = Person('John', 78)
p2 = Person('John', 78)
print(id(p1) is id(p2))
print(p1 == p2)
print(hash(p1) == hash(p2))


# As you can see, `Person` objects are now hashable, and equal objects have equal hashes. Of course, if the objects are not equal they usually will have different hashes (though that is not mandatory - we'll come back to that in a bit).

# In[37]:


p3 = Person('Eric', 75)


# In[38]:


print(p1 == p3)
print(hash(p1) == hash(p3))


# Let's just remove that print statement quick:

# In[39]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        else:
            return False
    
    def __hash__(self):
        return hash((self.name, self.age))


# Now let's see how this works with dictionaries:

# In[40]:


p1 = Person('John', 78)
p2 = Person('John', 78)
p3 = Person('Eric', 75)


# In[41]:


persons = {p1: 'first John object'}


# In[42]:


persons[p1]


# In[43]:


persons[p2]


# In[44]:


persons[p3]


# Now let's try to add `p2` to the dictionary:

# In[45]:


persons[p2] = 'other (equal) John object'


# In[46]:


persons


# As you can see, we actually just overwrote the value of that key - since those two keys are in fact equal (`==`).

# So we could not do this:

# In[47]:


persons = {p1: 'p1', p2: 'p2'}


# In[48]:


persons


# As you can see the key was considered the same, and hence the last value assignment was effective.

# But of course we could do this:

# In[49]:


persons = {p1: 'p1', p3: 'p3'}


# In[50]:


persons


# since `p1` and `p3` are not equal (`==`).

# ##### A subtle point about ` __hash__` and `hash()`

# The `__hash__` method must return an integer - Python will complain otherwise:

# In[51]:


class Test:
    def __hash__(self):
        return 'a string'


# In[52]:


hash(Test())


# Just out of interest:
# 
# When we call the `hash()` function, although it in turn calls the `__hash__` method, it does something more.
# 
# It will truncate the integer returned by `__hash__` to a certain width which is implementation dependent.
# 
# In my case, I can see that hashes will be truncated to 64-bits:

# In[53]:


import sys
sys.hash_info.width


# Let's just see how that affects the results of our `__hash__` method:

# In[54]:


class Test:
    def __hash__(self):
        return 1_000_000_000_000_000_000


# In[55]:


hash(Test())


# In[56]:


class Test:
    def __hash__(self):
        return 10_000_000_000_000_000_000


# In[57]:


hash(Test())


# In[58]:


mod = sys.hash_info.modulus


# In[59]:


mod


# In[60]:


10_000_000_000_000_000_000 % mod


# ##### Back to equal hashes for unequal objects

# As we have seen many times now, hash functions and hashable objects need to satisfy these conditions:
# 1. if a == b then hash(a) == hash(b)
# 2. hash(a) must be an integer
# 
# But nothing specifies here that unequal objects must result in unequal hashes.
# 
# The only issue with equal hashes with unequal objects is that we end up getting more collisions when looking up a key in a dictionary (refer to the earlier theory section if you want more details on this)

# So, let's try it out with our `Person` class, we are going to implement a hash that is going to be a constant integer. That will still satisfy conditions (1) and (2) above:

# In[61]:


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return f'Person(name={self.name}, age={self.age})'
    
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        else:
            return False
    
    def __hash__(self):
        return 100


# In[62]:


p1 = Person('John', 78)
p2 = Person('Eric', 75)


# In[63]:


hash(p1), hash(p2)


# In[64]:


p1 == p2


# In[65]:


persons = {p1: 'p1', p2: 'p2'}


# In[66]:


persons


# In[67]:


persons[p1]


# In[68]:


persons[p2]


# In[69]:


persons[Person('John', 78)]


# As you can see that still works just fine.
# But let's see how performance is affected by this.
# To test this we are going to create a slightly simpler class:

# In[70]:


class Number:
    def __init__(self, x):
        self.x = x
        
    def __eq__(self, other):
        if isinstance(other, Number):
            return self.x == other.x
        else:
            return False
    
    def __hash__(self):
        return hash(self.x)        


# In[71]:


class SameHash:
    def __init__(self, x):
        self.x = x
        
    def __eq__(self, other):
        if isinstance(other, SameHash):
            return self.x == other.x
        else:
            return False
    
    def __hash__(self):
        return 100   


# In[72]:


numbers = {Number(i): 'some value' for i in range(1_000)}
same_hashes = {SameHash(i): 'some value' for i in range(1_000)}


# In[73]:


numbers[Number(500)]


# In[74]:


same_hashes[SameHash(500)]


# And now let's time how long it takes to retrieve an element from each of those dictionaries:

# In[75]:


from timeit import timeit


# In[76]:


print(timeit('numbers[Number(500)]', globals=globals(), number=10_000))


# In[77]:


print(timeit('same_hashes[SameHash(500)]', globals=globals(), number=10_000))


# As you can see it takes substantially longer (by a factor of more than 100x) to look up a value when we have hash collisions.
# In fact this is the reason why Python has randomized hashes for strings, dates, and a few other built in types. If these hashes were predictable it would be easy for an attacker to purposefully provide keys with the same hash to slow down the system in a denial of service attack.

# So, even though that constant value we provide for a hash is technically valid, I wouldn't recommend you use something like it!!

# #### Example

# Let's take a look at another practical example of where we might want to use custom hashing.
# 
# Let's say we want to write a custom class to handle 2D coordinates:

# In[78]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'({self.x}, {self.y})'


# In[79]:


pt = Point(1, 2)
print(pt)


# In this case, we actually would like to be able to put these points as keys in a dictionary.
# We certainly can as it is:

# In[80]:


points = {Point(0,0): 'pt 1', Point(1,1): 'pt 2'}


# But how do we recover the value for the point (0,0) for example?

# In[81]:


points[Point(0,0)]


# The problem of course is that Python is using a hash of the id of the points - so we need to implement a custom hash mechanism, and of course also the `__eq__` method (just because the hash of two objects is the same does not mean the objects are also equal, so to look up a key in a dictionary Python needs both a hash and equality).

# In[82]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False
        
    def __hash__(self):
        return hash((self.x, self.y))


# In[83]:


points = {Point(0, 0): 'origin', Point(1,1): 'pt at (1,1)'}


# In[84]:


points[Point(0,0)]


# As you can see we now have the desired functionality.
# 
# Let's actually take this a step further, and implement things in such a way that we could use a regular 2-element tuple to look up a point in the dictionary.
# 
# To do this we'll have to make sure that `(x, y) == Point(x, y)` and of course make sure that in that case we also have equal hashes - but since we are already calculating the hash of a Point as the hash of the corresponding tuple, we're already fine there.

# In[85]:


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            other = Point(*other)
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False
        
    def __hash__(self):
        return hash((self.x, self.y))


# In[86]:


points = {Point(0,0): 'origin', Point(1,1): 'pt at (1,1)'}


# In[87]:


points[Point(0,0)]


# In[88]:


points[(0,0)]


# In fact:

# In[89]:


(0,0) == Point(0,0)


# You'll notice that our `Point` class is technically mutable.
# So we could do something like this:

# In[90]:


pt1 = Point(0,0)
pt2 = Point(1,1)
points = {pt1: 'origin', pt2: 'pt at (1,1)'}


# In[91]:


points[pt1], points[Point(0,0)], points[(0,0)]


# But what happens if we mutate `pt1`?

# In[92]:


pt1.x = 10


# In[93]:


pt1


# In[94]:


points[pt1]


# So we can't recover our item using `pt1`, that's because the hash of `pt1` has changed, so Python start looking in the wrong place in the dictionary.
# 
# Let's see what the items are in the dictionary:

# In[95]:


for k, v in points.items():
    print(k, v)


# So can we recover that 'origin' point using a different key maybe?

# In[96]:


points[Point(10, 0)]


# Also not, again because the hash under which the original point `pt1` was stored, is not the same as the new hash for that same object.
# 
# This is why we should not use mutable keys in a dictionary!
# 
# So, in this case, although we cannot technically enfore immutability, we can use conventions to indicate the object is supposed to be immutable:

# In[97]:


class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __repr__(self):
        return f'({self.x}, {self.y})'
    
    def __eq__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            other = Point(*other)
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False
        
    def __hash__(self):
        return hash((self.x, self.y))


# Everything works just as before, but making the underlying attributes `_x` and `_y` indicates these are private and should not be modified directly.
# Furthermore we only created attribute getters, not setters for `x` and `y`:

# In[98]:


pt = Point(0,0)


# In[99]:


pt.x


# In[100]:


pt.x = 10

