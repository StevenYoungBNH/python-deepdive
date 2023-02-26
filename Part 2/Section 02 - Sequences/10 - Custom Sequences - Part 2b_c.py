#!/usr/bin/env python
# coding: utf-8

# ### Custom Sequences (Part 2b/c)

# For this example we'll re-use the Polygon class from a previous lecture on extending sequences.
# 
# We are going to consider a polygon as nothing more than a collection of points (and we'll stick to a 2-dimensional space).
# 
# So, we'll need a `Point` class, but we're going to use our own custom class instead of just using a named tuple.
# 
# We do this because we want to enforce a rule that our Point co-ordinates will be real numbers. We would not be able to use a named tuple to do that and we could end up with points whose `x` and `y` coordinates could be of any type.

# First we'll need to see how we can test if a type is a numeric real type.
# 
# We can do this by using the numbers module.

# In[1]:


import numbers


# This module contains certain base types for numbers that we can use, such as Number, Real, Complex, etc.

# In[2]:


isinstance(10, numbers.Number)


# In[3]:


isinstance(10.5, numbers.Number)


# In[4]:


isinstance(1+1j, numbers.Number)


# We will want our points to be real numbers only, so we can do it this way:

# In[5]:


isinstance(1+1j, numbers.Real)


# In[6]:


isinstance(10, numbers.Real)


# In[7]:


isinstance(10.5, numbers.Real)


# So now let's write our Point class. We want it to have these properties:
# 
#   1. The `x` and `y` coordinates should be real numbers only
#   2. Point instances should be a sequence type so that we can unpack it as needed in the same way we were able to unpack the values of a named tuple.

# In[8]:


class Point:
    def __init__(self, x, y):
        if isinstance(x, numbers.Real) and isinstance(y, numbers.Real):
            self._pt = (x, y)
        else:
            raise TypeError('Point co-ordinates must be real numbers.')
            
    def __repr__(self):
        return f'Point(x={self._pt[0]}, y={self._pt[1]})'
    
    def __len__(self):
        return 2
    
    def __getitem__(self, s):
        return self._pt[s]


# Let's use our point class and make sure it works as intended:

# In[9]:


p = Point(1, 2)


# In[10]:


p


# In[11]:


len(p)


# In[13]:


p[0], p[1]


# In[14]:


x, y = p


# In[15]:


x, y


# Now, we can start creatiung our Polygon class, that will essentially be a mutable sequence of points making up the verteces of the polygon.

# In[21]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        return f'Polygon({self._pts})'


# Let's try it and see if everything is as we expect:

# In[22]:


p = Polygon()


# In[23]:


p


# In[24]:


p = Polygon((0,0), [1,1])


# In[25]:


p


# In[26]:


p = Polygon(Point(0, 0), [1, 1])


# In[27]:


p


# That seems to be working, but only one minor thing - our representation contains those square brackets which technically should not be there as the Polygon class init assumes multiple arguments, not a single iterable.
# 
# So we should fix that:

# In[37]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join(self._pts)
        return f'Polygon({pts_str})'


# But that still won't work, because the `join` method expects an iterable of **strings** - here we are passing it an iterable of `Point` objects:

# In[29]:


p = Polygon((0,0), (1,1))


# In[30]:


p


# So, let's fix that:

# In[34]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'


# In[35]:


p = Polygon((0,0), (1,1))


# In[36]:


p


# Ok, so now we can start making our Polygon into a sequence type, by implementing methods such as `__len__` and `__getitem__`:

# In[39]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]


# Notice how we are simply delegating those methods to the ones supported by lists since we are storing our sequence of points internally using a list!

# In[40]:


p = Polygon((0,0), Point(1,1), [2,2])


# In[41]:


p


# In[42]:


p[0]


# In[43]:


p[::-1]


# Now let's implement concatenation (we'll skip repetition - wouldn't make much sense anyway):

# In[45]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, other):
        if isinstance(other, Polygon):
            new_pts = self._pts + other._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')


# In[47]:


p1 = Polygon((0,0), (1,1))
p2 = Polygon((2,2), (3,3))
print(id(p1), p1)
print(id(p2), p2)


# In[48]:


result = p1 + p2


# In[49]:


print(id(result), result)


# Now, let's handle in-place concatenation. Let's start by only allowing the RHS of the in-place concatenation to be another Polygon:

# In[71]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, other):
        if isinstance(other, Polygon):
            new_pts = self._pts + other._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
            
    def __iadd__(self, pt):
        if isinstance(pt, Polygon):
            self._pts = self._pts + pt._pts
            return self
        else:
            raise TypeError('can only concatenate with another Polygon')


# In[72]:


p1 = Polygon((0,0), (1,1))
p2 = Polygon((2,2), (3,3))
print(id(p1), p1)
print(id(p2), p2)


# In[73]:


p1 += p2


# In[74]:


print(id(p1), p1)


# So that worked, but this would not:

# In[75]:


p1 = Polygon((0,0), (1,1))


# In[76]:


p1 += [(2,2), (3,3)]


# As you can see we get that type error. But we really should be able to handle appending any iterable of Points - and of course Points could also be specified as just iterables of length 2 containing numbers:

# In[77]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
            
    def __iadd__(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
        return self


# In[78]:


p1 = Polygon((0,0), (1,1))


# In[79]:


p1 += [(2,2), (3,3)]


# In[80]:


p1


# Now let's implement some methods such as `append`, `extend` and `insert`:

# In[81]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
            
    def __iadd__(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
        return self
    
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
            
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))


# Notice how we used almost the same code for `__iadd__` and `extend`?
# The only difference is that `__iadd__` returns the object, while `extend` does not - so let's clean that up a bit:

# In[82]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))


# Now let's give all this a try:

# In[93]:


p1 = Polygon((0,0), Point(1,1))
p2 = Polygon([2, 2], [3, 3])
print(id(p1), p1)
print(id(p2), p2)


# In[94]:


p1 += p2


# In[95]:


print(id(p1), p1)


# That worked still, now let's see `append`:

# In[96]:


p1


# In[97]:


p1.append((4, 4))


# In[98]:


p1


# In[99]:


p1.append(Point(5,5))


# In[104]:


print(id(p1), p1)


# `append` seems to be working, now for `extend`:

# In[101]:


p3 = Polygon((6,6), (7,7))


# In[102]:


p1.extend(p3)


# In[103]:


print(id(p1), p1)


# In[106]:


p1.extend([(8,8), Point(9,9)])


# In[107]:


print(id(p1), p1)


# Now let's see if `insert` works as expected:

# In[108]:


p1 = Polygon((0,0), (1,1), (2,2))


# In[109]:


print(id(p1), p1)


# In[110]:


p1.insert(1, (100, 100))


# In[111]:


print(id(p1), p1)


# In[112]:


p1.insert(1, Point(50, 50))


# In[113]:


print(id(p1), p1)


# Now that we have that working, let's turn our attention to the `__setitem__` method so we can support index and slice assignments:

# In[114]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # value could be a single Point (or compatible type) for s an int
        # or it could be an iterable of Points if s is a slice
        # let's start by handling slices only first
        self._pts[s] = [Point(*pt) for pt in value]
            
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))


# So, we are only handling slice assignments at this point, not assignments such as `p[0] = Point(0,0)`:

# In[117]:


p = Polygon((0,0), (1,1), (2,2))
print(id(p), p)


# In[118]:


p[0:2] = [(10, 10), (20, 20), (30, 30)]


# In[119]:


print(id(p), p)


# So this seems to work fine. But this won't yet:

# In[120]:


p[0] = Point(100, 100)


# If we look at the precise error, we see that our list comprehension is the cause of the error - we fail to correctly handle the case where the value passed in is not an iterable of Points...

# In[124]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # value could be a single Point (or compatible type) for s an int
        # or it could be an iterable of Points if s is a slice
        # we could do this:
        if isinstance(s, int):
            self._pts[s] = Point(*value)
        else:
            self._pts[s] = [Point(*pt) for pt in value]
            
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))


# This will now work as expected:

# In[125]:


p = Polygon((0,0), (1,1), (2,2))
print(id(p), p)


# In[126]:


p[0] = Point(10, 10)


# In[127]:


print(id(p), p)


# What happens if we try to assign a single Point to a slice:

# In[128]:


p[0:2] = Point(10, 10)


# As expected this will not work. What about assigning an iterable of points to an index:

# In[130]:


p[0] = [Point(10, 10), Point(20, 20)]


# This works fine, but the error messages are a bit misleading - we probably should do something about that:

# In[162]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # we first should see if we have a single Point
        # or an iterable of Points in value
        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            # not a valid iterable of Points
            # maybe a single Point?
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                # still no go
                raise TypeError('Invalid Point or iterable of Points')
        
        # reached here, so rhs is either an iterable of Points, or a Point
        # we want to make sure we are assigning to a slice only if we 
        # have an iterable of points, and assigning to an index if we 
        # have a single Point only
        if (isinstance(s, int) and is_single) \
            or isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError('Incompatible index/slice assignment')
                
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))


# So now let's see if we get better error messages:

# In[154]:


p1 = Polygon((0,0), (1,1), (2,2))


# In[155]:


p1[0:2] = (10,10)


# In[156]:


p1[0] = [(0,0), (1,1)]


# And the allowed slice/index assignments work as expected:

# In[157]:


p[0] = Point(100, 100)


# In[158]:


p


# In[159]:


p[0:2] = [(0,0), (1,1), (2,2)]


# In[160]:


p


# And if we try to replace with bad Point data:

# In[161]:


p[0] = (0, 2+2j)


# We also get a better error message.

# Lastly let's see how we would implement the `del` keyword and the `pop` method.

# Recall how the `del` keyword works for a list:

# In[163]:


l = [1, 2, 3, 4, 5]


# In[164]:


del l[0]


# In[165]:


l


# In[166]:


del l[0:2]


# In[167]:


l


# In[168]:


del l[-1]


# In[169]:


l


# So, `del` works with indices (positive or negative) and slices too. We'll do the same:

# In[180]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # we first should see if we have a single Point
        # or an iterable of Points in value
        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            # not a valid iterable of Points
            # maybe a single Point?
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                # still no go
                raise TypeError('Invalid Point or iterable of Points')
        
        # reached here, so rhs is either an iterable of Points, or a Point
        # we want to make sure we are assigning to a slice only if we 
        # have an iterable of points, and assigning to an index if we 
        # have a single Point only
        if (isinstance(s, int) and is_single) \
            or isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError('Incompatible index/slice assignment')
                
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
        
    def __delitem__(self, s):
        del self._pts[s]


# In[181]:


p = Polygon(*zip(range(6), range(6)))


# In[182]:


p


# In[183]:


del p[0]


# In[184]:


p


# In[185]:


del p[-1]


# In[186]:


p


# In[187]:


del p[0:2]


# In[188]:


p


# Now, we just have to implement `pop`:

# In[189]:


class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # we first should see if we have a single Point
        # or an iterable of Points in value
        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            # not a valid iterable of Points
            # maybe a single Point?
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                # still no go
                raise TypeError('Invalid Point or iterable of Points')
        
        # reached here, so rhs is either an iterable of Points, or a Point
        # we want to make sure we are assigning to a slice only if we 
        # have an iterable of points, and assigning to an index if we 
        # have a single Point only
        if (isinstance(s, int) and is_single) \
            or isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError('Incompatible index/slice assignment')
                
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
        
    def __delitem__(self, s):
        del self._pts[s]
        
    def pop(self, i):
        return self._pts.pop(i)


# In[190]:


p = Polygon(*zip(range(6), range(6)))


# In[191]:


p


# In[192]:


p.pop(1)


# In[193]:


p

