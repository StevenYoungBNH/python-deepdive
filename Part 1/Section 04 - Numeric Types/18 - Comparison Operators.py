#!/usr/bin/env python
# coding: utf-8

# ### Comparison Operators

# #### Identity and Membership Operators

# The **is** and **is not** operators will work with any data type since they are comparing the memory addresses of the objects (which are integers)

# In[3]:


0.1 is (3+4j)


# In[4]:


'a' is [1, 2, 3]


# The **in** and **not in** operators are used with iterables and test membership:

# In[5]:


1 in [1, 2, 3]


# In[6]:


[1, 2] in [1, 2, 3]


# In[7]:


[1, 2] in [[1,2], [2,3], 'abc']


# In[8]:


'key1' in {'key1': 1, 'key2': 2}


# In[9]:


1 in {'key1': 1, 'key2': 2}


# We'll come back to these operators in later sections on iterables and mappings.

# #### Equality Operators

# The **==** and **!=** operators are value comparison operators. 
# 
# They will work with mixed types that are comparable in some sense.
# 
# For example, you can compare Fraction and Decimal objects, but it would not make sense to compare string and integer objects.

# In[10]:


1 == '1'


# In[11]:


from decimal import Decimal
from fractions import Fraction


# In[12]:


Decimal('0.1') == Fraction(1, 10)


# In[13]:


1 == 1 + 0j


# In[14]:


True == Fraction(2, 2)


# In[15]:


False == 0j


# #### Ordering Comparisons

# Many, but not all data types have an ordering defined.
# 
# For example, complex numbers do not.

# In[16]:


1 + 1j < 2 + 2j


# Mixed type ordering comparisons is supported, but again, it needs to make sense:

# In[17]:


1 < 'a'


# In[18]:


Decimal('0.1') < Fraction(1, 2)


# #### Chained Comparisons

# It is possible to chain comparisons.
# 
# For example, in **a < b < c**, Python simply **ands** the pairwise comparisons: **a < b and b < c**

# In[19]:


1 < 2 < 3


# In[20]:


1 < 2 > -5 < 50 > 4


# In[29]:


1 < 2 == Decimal('2.0')


# In[28]:


import string
'A' < 'a' < 'z' > 'Z' in string.ascii_letters 

