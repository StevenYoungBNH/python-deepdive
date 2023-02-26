#!/usr/bin/env python
# coding: utf-8

# ### Project Solution: Goal 2

# For this goal we need to rewrite our sequence type `Polygons` into something that implements the iterable protocol.
# 
# Furthermore, all iterators should be lazy.

# We'll need our `Polygon` class:

# In[1]:


import math

class Polygon:
    def __init__(self, n, R):
        if n < 3:
            raise ValueError('Polygon must have at least 3 vertices.')
        self._n = n
        self._R = R
        
        self._interior_angle = None
        self._side_length = None
        self._apothem = None
        self._area = None
        self._perimeter = None
        
    def __repr__(self):
        return f'Polygon(n={self._n}, R={self._R})'
    
    @property
    def count_vertices(self):
        return self._n
    
    @property
    def count_edges(self):
        return self._n
    
    @property
    def circumradius(self):
        return self._R
    
    @property
    def interior_angle(self):
        if self._interior_angle is None:
            self._interior_angle = (self._n - 2) * 180 / self._n
        return self._interior_angle

    @property
    def side_length(self):
        if self._side_length is None:
            self._side_length = 2 * self._R * math.sin(math.pi / self._n)
        return self._side_length
    
    @property
    def apothem(self):
        if self._apothem is None:
            self._apothem = self._R * math.cos(math.pi / self._n)
        return self._apothem
    
    @property
    def area(self):
        if self._area is None:
            self._area = self._n / 2 * self.side_length * self.apothem
        return self._area
    
    @property
    def perimeter(self):
        if self._perimeter is None:
            self._perimeter = self._n * self.side_length
        return self._perimeter
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.count_edges == other.count_edges 
                    and self.circumradius == other.circumradius)
        else:
            return NotImplemented
        
    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.count_vertices > other.count_vertices
        else:
            return NotImplemented


# And here's our original implementation of `Polygons` as a sequence type:

# In[2]:


class Polygons:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R
        self._polygons = [Polygon(i, R) for i in range(3, m+1)]
        
    def __len__(self):
        return self._m - 2
    
    def __repr__(self):
        return f'Polygons(m={self._m}, R={self._R})'
    
    def __getitem__(self, s):
        return self._polygons[s]
    
    @property
    def max_efficiency_polygon(self):
        sorted_polygons = sorted(self._polygons, 
                                 key=lambda p: p.area/p.perimeter,
                                reverse=True)
        return sorted_polygons[0]


# We now need to implement the iterable protocol - which means we'll need to implement an iterator first.

# In[3]:


class PolygonsIterator:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R
        
    def __iter__(self):
        return self
    
    def __next__(self):
        pass


# This is the basic skeleton we need to implement the iterator protocol.
# 
# So now we need to implement the __next__ method.
# 
# This method should simply return the `next` instance of a Polygon - we start with polygons with `3` sides, and work our way up.
# 
# To do this, we'll use a private variable `_i` to trqack the number-of-side Polygon to hand out next. So, we'll start `_i` at `3` and work our way up.

# In[4]:


class PolygonsIterator:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R
        self._i = 3
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._i > self._m:
            raise StopIteration
        else:
            result = Polygon(self._i, self._R)
            self._i += 1
            return result


# Let's make sure the iterator works as expected:

# In[5]:


p_iter = PolygonsIterator(5, 1)
for p in p_iter:
    print(p)


# Of course, this is an iterator, so it should be exhausted now:

# In[6]:


list(p_iter)


# Looks good, so next we have to replace the sequence protocol with the iterable protocol in our `Polygons` class.

# In[7]:


class Polygons:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R
        
    def __len__(self):
        return self._m - 2
    
    def __repr__(self):
        return f'Polygons(m={self._m}, R={self._R})'
    
    def __iter__(self):
        return PolygonsIterator(self._m, self._R)
    
    @property
    def max_efficiency_polygon(self):
        sorted_polygons = sorted(self._polygons, 
                                 key=lambda p: p.area/p.perimeter,
                                reverse=True)
        return sorted_polygons[0]


# And now we should have an iterable:

# In[8]:


polygons = Polygons(5, 1)


# In[9]:


for p in polygons:
    print(p)


# In[10]:


for p in polygons:
    print(p)


# Finally, we also need to make our `max_efficiency_polygon` a lazy property:

# In[11]:


class Polygons:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R
        self._max_efficiency_polygon = None
        
    def __len__(self):
        return self._m - 2
    
    def __repr__(self):
        return f'Polygons(m={self._m}, R={self._R})'
    
    def __iter__(self):
        return PolygonsIterator(self._m, self._R)
    
    @property
    def max_efficiency_polygon(self):
        if self._max_efficiency_polygon is None:
            sorted_polygons = sorted(self._polygons, 
                                     key=lambda p: p.area/p.perimeter,
                                    reverse=True)
            self._max_efficiency_polygon = sorted_polygons[0]
        return self._max_efficiency_polygon


# Let's test that to make sure it still calculates correctly (should always return the largest (in terms of edges/vertices) Polygon in the iterable.

# In[12]:


polygons = Polygons(10, 1)
print(polygons.max_efficiency_polygon)


# As you can see, we have a slight problem. We also need to change the iterable passed to the `sorted` method - we no longer have a list of Polygons.
# 
# But that's easily fixed since `sorted` can work with iterables and iterators in general!

# In[13]:


class Polygons:
    def __init__(self, m, R):
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R
        self._max_efficiency_polygon = None
        
    def __len__(self):
        return self._m - 2
    
    def __repr__(self):
        return f'Polygons(m={self._m}, R={self._R})'
    
    def __iter__(self):
        return PolygonsIterator(self._m, self._R)
    
    @property
    def max_efficiency_polygon(self):
        if self._max_efficiency_polygon is None:
            sorted_polygons = sorted(PolygonsIterator(self._m, self._R), 
                                     key=lambda p: p.area/p.perimeter,
                                    reverse=True)
            self._max_efficiency_polygon = sorted_polygons[0]
        return self._max_efficiency_polygon


# And let's test that again:

# In[14]:


polygons = Polygons(10, 1)
print(polygons.max_efficiency_polygon)


# OK, that seems to work!
