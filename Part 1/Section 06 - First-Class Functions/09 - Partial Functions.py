#!/usr/bin/env python
# coding: utf-8

# ### Partial Functions

# In[1]:


from functools import partial


# In[2]:


def my_func(a, b, c):
    print(a, b, c)


# In[3]:


f = partial(my_func, 10)


# In[4]:


f(20, 30)


# We could have done this using another function (or a lambda) as well:

# In[5]:


def partial_func(b, c):
    return my_func(10, b, c)


# In[6]:


partial_func(20, 30)


# or, using a lambda:

# In[7]:


fn = lambda b, c: my_func(10, b, c)


# In[8]:


fn(20, 30)


# Any of these ways is fine, but sometimes partial is just a cleaner more consise way to do it.
# 
# Also, it is quite flexible with parameters:

# In[9]:


def my_func(a, b, *args, k1, k2, **kwargs):
    print(a, b, args, k1, k2, kwargs)


# In[10]:


f = partial(my_func, 10, k1='a')


# In[11]:


f(20, 30, 40, k2='b', k3='c')


# We can of course do the same thing using a regular function too:

# In[12]:


def f(b, *args, k2, **kwargs):
    return my_func(10, b, *args, k1='a', k2=k2, **kwargs)


# In[13]:


f(20, 30, 40, k2='b', k3='c')


# As you can see in this case, using **partial** seems a lot simpler.

# Also, you are not stuck having to specify the first argument in your partial:

# In[14]:


def power(base, exponent):
    return base ** exponent


# In[15]:


power(2, 3)


# In[16]:


square = partial(power, exponent=2)


# In[17]:


square(4)


# In[18]:


cube = partial(power, exponent=3)


# In[19]:


cube(2)


# You can even call it this way:

# In[20]:


cube(base=3)


# #### Caveat

# We can certainly use variables instead of literals when creating partials, but we have to be careful.

# In[21]:


def my_func(a, b, c):
    print(a, b, c)


# In[22]:


a = 10
f = partial(my_func, a)


# In[23]:


f(20, 30)


# Now let's change the value of the variable **a** and see what happens:

# In[24]:


a = 100


# In[25]:


f(20, 30)


# As you can see, the value for **a** is fixed once the partial has been created.
# 
# In fact, the memory address of **a** is baked in to the partial, and **a** is immutable.

# If we use a mutable object, things are different:

# In[26]:


a = [10, 20]
f = partial(my_func, a)


# In[27]:


f(100, 200)


# In[28]:


a.append(30)


# In[29]:


f(100, 200)


# #### Use Cases

# We tend to use partials in situation where we need to call a function that actually requires more parameters than we can supply.
# 
# Often this is because we are working with exiting libraries or code, and we have a special case.

# For example, suppose we have points (represented as tuples), and we want to sort them based on the distance of the point from some other fixed point:

# In[30]:


origin = (0, 0)


# In[31]:


l = [(1,1), (0, 2), (-3, 2), (0,0), (10, 10)]


# In[32]:


dist2 = lambda x, y: (x[0]-y[0])**2 + (x[1]-y[1])**2


# In[33]:


dist2((0,0), (1,1))


# In[34]:


sorted(l, key = lambda x: dist2((0,0), x))


# In[35]:


sorted(l, key=partial(dist2, (0,0)))


# Another use case is when using **callback** functions. Usually these are used when running asynchronous operations, and you provide a callable to another callable which will be called when the first callable completes its execution.
# 
# Very often, the asynchronous callable will specify the number of variables that the callback function must have - this may not be what we want, maybe we want to add some additional info.

# We'll look at asynchronous processing later in this course.

# Often we can also use partial functions to make our life a bit easier.
# 
# Consider a situation where we have some generic `email()` function that can be used to notify someone when various things happen in our application. But depending on what is happening we may want to notify different people. Let's see how we may do this:

# In[36]:


def sendmail(to, subject, body):
    # code to send email
    print('To:{0}, Subject:{1}, Body:{2}'.format(to, subject, body))


# Now, we may haver different email adresses we want to send notifications to, maybe defined in a config file in our app. Here, I'll just use hardcoded variables:

# In[37]:


email_admin = 'palin@python.edu'
email_devteam = 'idle@python.edu;cleese@python.edu'


# Now when we want to send emails we would have to write things like:

# In[38]:


sendmail(email_admin, 'My App Notification', 'the parrot is dead.')
sendmail(';'.join((email_admin, email_devteam)), 'My App Notification', 'the ministry is closed until further notice.')


# We could simply our life a little using partials this way:

# In[39]:


send_admin = partial(sendmail, email_admin, 'For you eyes only')
send_dev = partial(sendmail, email_devteam, 'Dear IT:')
send_all = partial(sendmail, ';'.join((email_admin, email_devteam)), 'Loyal Subjects')


# In[40]:


send_admin('the parrot is dead.')
send_all('the ministry is closed until further notice.')


# Finally, let's make this a little more complex, with a mixture of positional and keyword-only arguments:

# In[41]:


def sendmail(to, subject, body, *, cc=None, bcc=email_devteam):
    # code to send email
    print('To:{0}, Subject:{1}, Body:{2}, CC:{3}, BCC:{4}'.format(to, 
                                                                  subject, 
                                                                  body, 
                                                                  cc, 
                                                                  bcc))


# In[42]:


send_admin = partial(sendmail, email_admin, 'General Admin')
send_admin_secret = partial(sendmail, email_admin, 'For your eyes only', cc=None, bcc=None)


# In[43]:


send_admin('and now for something completely different')


# In[44]:


send_admin_secret('the parrot is dead!')


# In[45]:


send_admin_secret('the parrot is no more!', bcc=email_devteam)


# In[49]:


def pow(base, exponent):
    return base ** exponent


# In[52]:


cube = partial(pow, exponent=3)


# In[53]:


cube(2)


# In[54]:


cube(2, 4)


# In[55]:


cube(2, exponent=4)


# In[ ]:




