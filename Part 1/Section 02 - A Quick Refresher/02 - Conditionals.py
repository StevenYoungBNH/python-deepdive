#!/usr/bin/env python
# coding: utf-8

# ### Conditionals

# A conditional is a construct that allows you to branch your code based on conditions being met (or not)

# This is achieved using **if**, **elif** and **else** or the **ternary operator** (aka conditional expression)

# In[2]:


a = 2
if a < 3:
    print('a < 3')
else:
    print('a >= 3')


# **if** statements can be nested:

# In[7]:


a = 15

if a < 5:
    print('a < 5')
else:
    if a < 10:
        print('5 <= a < 10')
    else:
        print('a >= 10')


# But the **elif** statement provides far better readability:

# In[8]:


a = 15
if a < 5:
    print('a < 5')
elif a < 10:
    print('5 <= a < 10')
else:
    print('a >= 10')


# In Python, **elif** is the closest you'll find to the switch/case statement available in some other languages.

# Python also provides a conditional expression (ternary operator):
# 
# X if (condition) else Y
# 
# returns (and evaluates) X if (condition) is True, otherwise returns (and evaluates) Y

# In[1]:


a = 5
res = 'a < 10' if a < 10 else 'a >= 10'
print(res)


# In[13]:


a = 15
res = 'a < 10' if a < 10 else 'a >= 10'
print(res)


# Note that **X** and **Y** can be any expression, not just literal values:

# In[15]:


def say_hello():
    print('Hello!')
    
def say_goodbye():
    print('Goodbye!')


# In[16]:


a = 5
say_hello() if a < 10 else say_goodbye()


# In[17]:


a = 15
say_hello() if a < 10 else say_goodbye()

