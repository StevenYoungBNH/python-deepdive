#!/usr/bin/env python
# coding: utf-8

# ### Booleans

# The **bool** class is used to represent boolean values.

# The **bool** class inherits from the **int** class.

# In[1]:


issubclass(bool, int)


# Two built-in constants, **True** and **False** are singleton instances of the bool class with underlying int values of 1 and 0 respectively.

# In[7]:


type(True), id(True), int(True)


# In[8]:


type(False), id(False), int(False)


# These two values are instances of the **bool** class, and by inheritance are also **int** objects.

# In[5]:


isinstance(True, bool)


# In[6]:


isinstance(True, int)


# Since **True** and **False** are singletons, we can use either the **is** operator, or the **==** operator to compare them to **any** boolean expression.

# In[9]:


id(True), id(1 < 2)


# In[10]:


id(False), id(1 == 3)


# In[12]:


(1 < 2) is True, (1 < 2) == True


# In[13]:


(1 == 2) is False, (1 == 2) == False


# Be careful with that last comparison, the parentheses are necessary!

# In[15]:


1 == 2 == False


# In[16]:


(1 == 2) == False


# We'll look into this in detail later, but, for now, this happens because a chained comparison such as **a == b == c** is actually evaluated as **a == b and b == c**

# So **1 == 2 == False ** is the same as **1 == 2 and 2 == False**

# In[17]:


1 == 2, 2 == False, 1==2 and 2==False


# But, 

# In[18]:


(1 == 2)


# So **(1 == 2) == False** evaluates to True

# But since **False** is also **0**, we get the following:

# In[36]:


(1 == 2) == 0


# The underlying integer values of True and False are:

# In[19]:


int(True), int(False)


# So, using an equality comparison:

# In[20]:


1 == True, 0 == False


# But, from an object perspective 1 and True are not the same (similarly with 0 and False)

# In[21]:


1 == True, 1 is True


# In[23]:


0 == False, 0 is False


# Any integer can be cast to a boolean, and follows the rule:
# 
# bool(x) = True for any x except for zero which returns False

# In[24]:


bool(0)


# In[25]:


bool(1), bool(100), bool(-1)


# Since booleans are subclassed from integers, they can behave like integers, and because of polymorphism all the standard integer operators, properties and methods apply

# In[26]:


True > False


# In[27]:


True + 2


# In[29]:


False // 2


# In[33]:


True + True + True


# In[32]:


(True + True + True) % 2


# In[34]:


-True


# In[35]:


100 * False


# I certainly **do not** recommend you write code like that shown above, but be aware that it does work.
