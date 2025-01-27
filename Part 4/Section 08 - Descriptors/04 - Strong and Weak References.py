#!/usr/bin/env python
# coding: utf-8

# ### Strong and Weak References

# First let's bring back the function we can use to determine the reference count of an object by id:

# In[1]:


import ctypes

def ref_count(address):
    return ctypes.c_long.from_address(address).value


# Note that this counts the **strong** references to that object.

# So far, we have always worked with strong references. 

# In[2]:


class Person:
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f'Person(name={self.name})'


# In[3]:


p1 = Person('Guido')
p2 = p1


# In this case both `p1` and `p2` are **strong** references to the same `Person` instance (*Guido*).

# In[4]:


p1_id = id(p1)
p2_id = id(p2)


# In[5]:


p1_id == p2_id, ref_count(p1_id)


# So we have two strong references. If we delete one of them:

# In[6]:


del p2


# We should have a strong reference count of `1` now:

# In[7]:


ref_count(p1_id)


# We can delete the last reference:

# In[8]:


del p1


# Now our reference count function will not work anymore, since the last reference to the object at that memory address was removed and that memory address is now meaningless:

# In[9]:


ref_count(p1_id)


# So, the garbage collector will destroy any object whose **strong** reference count goes down to `0`.

# There is another type of reference to an object that we can use that **does not** affect the (strong) reference count - these are called **weak references**.

# We can create weak references to objects in Python using the `weakref` module:

# In[10]:


import weakref


# In[11]:


p1 = Person('Guido')


# In[12]:


p1_id = id(p1)


# In[13]:


ref_count(p1_id)


# Now let's make another strong reference:

# In[14]:


p2 = p1


# In[15]:


ref_count(p1_id)


# And finally let's make a weak reference to the same object:

# In[16]:


weak1 = weakref.ref(p1)


# Let's look at the ref count again:

# In[17]:


ref_count(p1_id)


# As you can see, it's still `2`.

# The `weak1` object is a weak reference object:

# In[18]:


weak1


# As you can see form the representation it is it's own object, but it points to the same object `p1` is currently pointing to:

# In[19]:


hex(p1_id)


# So `weak1` is not the `Person` instance:

# In[20]:


weak1 is p1


# In[21]:


ref_count(p1_id)


# But it is callable (so it implements a `__call__` method) that will return the object it is pointing to:

# In[22]:


weak1() is p1


# And we can see the object it is pointing to:

# In[23]:


print(weak1())


# Now we have to watch out here, if we did not use the `print` statement, Jupyter would be holding on to strong references to our object! Be sure to use `print` when using Jupyter...

# So our reference count should still be `2`:

# In[24]:


ref_count(p1_id)


# Another word of caution, if we do this:

# In[25]:


p3 = weak1()


# `p3` is now a strong reference to whatever object `weak1()` returned! In this case our *Guido* `Person`:

# In[26]:


p1 is p3


# In[27]:


ref_count(p1_id)


# And as you can see we now have three strong references.

# How many weak references do we have? We should have `1` only.
# 
# We can see how many weak references exist from some object by using the `getweakrefcount` function in the `weakref` module:

# In[28]:


weakref.getweakrefcount(p1), ref_count(p1_id)


# Another way of getting the strong ref count is in the `sys` module:

# In[29]:


import sys


# In[30]:


sys.getrefcount(p1)


# But you'll notice one thing, the ref count is increased by `1` - that's because we have to pass the object itself as an extra argument, so that's an extra strong reference! (so basically always subtract `1` from that ref count to get the true ref count)

# Now let's delete some of the strong references:

# In[31]:


del p3
del p2


# In[32]:


ref_count(p1_id)


# Our strong ref count is down to 1, and we still have one weak reference (`weak1`).

# Now let's delete the final strong reference:

# In[33]:


del p1


# Our strong ref count wnet down to `0`, so the garbage collector destroyed the object.

# So what happened to our weak reference?

# In[34]:


weak1


# The weak reference object still exists, but the object it is pointing to is **dead**.

# In fact, if we try to get the object, we will get `None` back:

# In[35]:


obj = weak1()


# In[36]:


obj is None


# As you can see, having a weak reference did not stop our object from being destroyed once all the strong references were gone.

# Note that not every object in Python supports weak references. Many of the built-in types do not:

# In[37]:


l = [1, 2, 3]
try:
    w = weakref.ref(l)
except TypeError as ex:
    print(ex)


# In[38]:


l = {'a': 1}
try:
    w = weakref.ref(l)
except TypeError as ex:
    print(ex)


# In[39]:


l = 100
try:
    w = weakref.ref(l)
except TypeError as ex:
    print(ex)


# In[40]:


l = 'python'
try:
    w = weakref.ref(l)
except TypeError as ex:
    print(ex)


# But our custom classes do, and that's what we need here.

# For our data descriptors, we want to use the instance objects as keys in our dictionary. But as we saw earlier, storing the object itself as the key can lead to memory leaks. So instead, we are going to store weak references to the object in the dictionary.

# We could use our own dictionary, but `weakref` also provides a specialized dictionary type, that will store a weak reference to the object being used as the key:

# In[41]:


p1 = Person('Guido')


# In[42]:


d = weakref.WeakKeyDictionary()


# In[43]:


ref_count(id(p1))


# In[44]:


weakref.getweakrefcount(p1)


# In[45]:


d[p1] = 'Guido'


# Now, notice the reference counts:

# In[46]:


ref_count(id(p1)), weakref.getweakrefcount(p1)


# We still have only one strong reference, but now we have a weak reference to `p1` as well! That weak reference is in the `WeakKeyDictionary`.

# We can easily see the weak references contained in that dictionary:

# In[47]:


hex(id(p1)), list(d.keyrefs())


# Now watch what happens to the dictionary when we delete the last strong reference to `p1`:

# In[48]:


del p1


# In[49]:


list(d.keyrefs())


# It was automatically removed when the object it was pointing to (weakly) was destroyed by the garbage collector!

# Now be careful, you can only use keys in the `WeakKeyDictionary` that Python can create weak references to:

# So this will not work:

# In[50]:


try:
    d['python'] = 'test'
except TypeError as ex:
    print(ex)


# Also, even though we are using a weak reference as a key in the dictionary, the object must still be **hashable**.
# 
# Let's see an example of this:

# In[51]:


class Person:
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        return isinstance(other, Person) and self.name == other.name


# Now `Person` is no longer hashable:

# In[52]:


p1 = Person('Guido')
p2 = Person('Guido')


# In[53]:


p1 == p2


# In[54]:


try:
    hash(p1)
except TypeError as ex:
    print(ex)


# And so we cannot use it as a key in our `WeakKeyDictionary`:

# In[55]:


try:
    d[p1] = 'Guido'
except TypeError as ex:
    print(ex)


# So we can certainly use `WeakKeyDictionary` objects in our data descriptors, but that will only work with hashable objects. In the next lectures we'll look at how to use `WeakKeyDictionary` as a storage mechanism for our data descriptors, as well as how to deal with the unhashable issue.
