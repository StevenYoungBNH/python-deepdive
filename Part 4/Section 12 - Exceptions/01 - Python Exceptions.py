#!/usr/bin/env python
# coding: utf-8

# ### Python Exceptions

# Exceptions are objects - instances of classes.

# In Python, all exceptions inherit from `BaseException`, but most of the majority of the builtin exceptions we work with derive from a subclass of that class, the `Exception` class.

# As I showed you in the lecture there is a hierarchy to those classes.

# When exceptions are `raised` (either by Python, or by ourselves), it triggers an exception workflow.

# Let's first see that exceptions are objects:

# In[1]:


type(Exception)


# In[2]:


ex = Exception()


# As you can see, creating an exception object does **not** trigger an exception workflow.

# Let's examine this `Exception` instance:

# In[3]:


ex.__class__, type(ex)


# And it is indeed a subclass of `BaseException`:

# In[4]:


isinstance(ex, BaseException)


# Other exceptions, such as an `IndexError`, inherit from a hierarchy of exceptions that go back all the way to `BaseException` (and `object` as well of course!)

# In[5]:


issubclass(IndexError, LookupError)


# In[6]:


issubclass(LookupError, Exception)


# Exception workflows can be triggered by Python itself:

# In[7]:


l = [1, 2, 3]
l[4]


# As you can see Python raised an `IndexError` exception.

# We can "handle" an exception workflow by using the a `try` statement and handling the exception (if any) in the `except` clause of the handler:

# In[8]:


try:
    l[4]
except IndexError as ex:
    print(ex.__class__, ':', str(ex))


# As you can see we **handled** the `IndexError` exception.

# But since `IndexError` inherits from `LookupError` which itself inherits from `Exception`, we could actually handle any of those exception types with the same effect:

# In[9]:


try:
    l[4]
except LookupError as ex:
    print(ex.__class__, ':', str(ex))


# As you may have noticed, the exception that is raised is **still** an `IndexError`, but it was handled by the `except LookupError` handler.

# So when we handle an exception, the handler will "catch" the exception type we specify, **and any subclass of it**.

# We can broaden our handler to include any subclass of `Exception`:

# In[10]:


try:
    l[4]
except Exception as ex:
    print(ex.__class__, ':', str(ex))


# But be careful of writing broad handlers like that - it is unlikely (but not always) that you can write handlers that do any meaningful error handling for such broad exceptions - the better approach is to handle specific exceptions in specific ways.

# By the way, most standard exceptions implement both `str` and `repr` custom representations:

# In[11]:


ex = ValueError('custom message')


# In[12]:


str(ex)


# In[13]:


repr(ex)


# Next we should talk about the stack trace. Recall what I mentioned in the lecture about exceptions propagating up if they are no handled.

# Let's start with an example of some nested function calls, and we'll raise an exception in the innermost function call.

# In[14]:


def func_1():
    func_2()
    
def func_2():
    func_3()
    
def func_3():
    # create an instance of a ValueError exception, and raise it
    raise ValueError()


# Now if I call `func_3` directly, we'll see an unhandled `ValueError` exception:

# In[15]:


func_3()


# But now let's call `func_1`:

# In[16]:


func_1()


# Notice the stack trace above. 
# 
# The bottom of the stack is where the exception started, then each "frame" above it tells us that the exception propagated - first to `func_2` (in the line that called `func_3`), and then finally in `func_1` (in the line that called `func_2`)

# Now of course we can handle the exception at any level we wish. When we handle an exception it is up to us to decide what to do with it - at that point we have interrupted the exception propagation, and we could either do something and continue running our code, or we could raise another exception, or we could re-raise the exception. We'll come back to that later.

# For now, let's see how we could handle the exception in `func_2` and silence it:

# In[17]:


def func_2():
    try:
        func_3()
    except ValueError:
        print('error occurred - silencing it')


# In[18]:


func_1()


# As you can see we essentially stopped the exception propagation in `func_2`.

# I just want to go back to the statement I made about not making our handlers too broad.

# Suppose we have a function that, given a sequence, returns the square of the numbers, up to (but not including) a specific index number in the sequence:

# In[19]:


def square(seq, index):
    return seq[index] ** 2

def squares(seq, max_n):
    for i in range(max_n):
        yield square(seq, i)


# Now if we have a problem with our max index, we'll get an `IndexError` exception:

# In[20]:


l = [1, 2, 3]


# In[21]:


list(squares(l, 4))


# So, we may want to trap that exception using a broad `Exception` handler:

# In[22]:


def square(seq, index):
    return seq[index] ** 2

def squares(seq, max_n):
    for i in range(max_n):
        try:
            yield square(seq, i)
        except Exception:
            return


# In[23]:


l = [1, 2, 3]
list(squares(l, 5))


# So that seems to work, and we can now deal with a bad max index. But what happens if I pass a seq where one of the values is not squarable?
# 
# This is the exception we should be seeing:

# In[24]:


'a' ** 2


# But watch what happens when we iterate:

# In[25]:


l = [1, 2, '3', 4, 5]
list(squares(l, 10))


# As you can see that exception was handled just like the index exception. That's probably not what I want - so it would be much better to write it this way:

# In[26]:


def square(seq, index):
    return seq[index] ** 2

def squares(seq, max_n):
    for i in range(max_n):
        try:
            yield square(seq, i)
        except IndexError:
            return


# In[27]:


l = [1, 2, '3', 4, 5]
list(squares(l, 10))


# And now I get an exception, which means I am aware of the problem, whereas the broad exception handler earlier completely hid from me.

# And of course this still works as expected:

# In[28]:


l = [1, 2, 3]
list(squares(l, 10))


# So be careful - broad exception handlers can easily hide bugs in your code. They are not recommended in practice, but are sometimes useful.

# For example, you might start a database transaction, and start writing some data to a database. 
# 
# Your application specs call for rolling back the transaction should **any** exception occur. 
# 
# In that case, a broad exception handler might make sense.
# 
# Better yet though, use a context manager!!

# In fact, we can make our exception handler even broader, by using a **bare** except:

# In[29]:


try:
    1 / 0
except:
    print('exception occurred')


# Again, not a good idea in general, but there are some valid use cases for this, which we'll see later.
