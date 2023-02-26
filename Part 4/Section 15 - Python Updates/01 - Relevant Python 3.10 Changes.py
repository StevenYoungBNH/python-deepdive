#!/usr/bin/env python
# coding: utf-8

# ### Relevant Python 3.10 Changes

# The release of Python 3.10 has brought some new features.
# 
# This is a summary of the ones _I_ deemed relevant to this course, and does **not** include all the changes!
# 
# For full release details, see [here](https://docs.python.org/3/whatsnew/3.10.html)

# Python 3.10 has improved it's error messages for syntax errors - the messages are more helpful and hopefully give you a better understanding of what may be syntactically wrong with your code.

# #### Structural Pattern Matching

# One thing I often hear people ask, is, what's the Python equivalent of a `switch` statement.

# Until now, the answer has alwasy been - there isn't one. Use `if...elif` constructs.

# Python 3.10 introduces a new language element (`match`) to implement something called **pattern matching**, that can be used to replicate this `switch` behavior you might be used to in other languages.

# I'll cover some of the basics here, but you should refer to the Python [docs](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement) for more information, as well as the [pep](https://peps.python.org/pep-0634/) for this feature and a [tutorial pep](https://peps.python.org/pep-0636/).

# Let's start with a simple `match` statement:

# In[1]:


def respond(language):
    match language:
        case "Java":
            return "Hmm, coffee!"
        case "Python":
            return "I'm not scared of snakes!"
        case "Rust":
            return "Don't drink too much water!"
        case "Go":
            return "Collect $200"
        case _:
            return "I'm sorry..."


# In[2]:


respond("Python")


# In[3]:


respond("Go")


# In[4]:


respond("COBOL")


# Here we were able to define a "default" match pattern by using the underscore (`_`) as our pattern - this `_` is called a **wildcard**.

# So this is very much like the "plain" switch statement found in some other languages.

# But, this is where things get ineteresting, pattern matching can do much more than the simple example we just saw.

# For example, you can have multiple pattern matching:

# In[5]:


def respond(language):
    match language:
        case "Java" | "Javascript":
            return "Love those braces!"
        case "Python":
            return "I'm a lumberjack and I don't need no braces"
        case _:
            return "I have no clue!"


# In[6]:


respond("Java")


# In[7]:


respond("Javascript")


# In[8]:


respond("Python")


# We could match against one or more literals by using the OR pattern (`|`)

# Let's look at one more example, this time matching **multiple values**.

# Suppose we have some kind of command language for driving a remote controlled robot in a maze, picking up and dropping items as it moves around. Our robot is very simple, it can move in only a few directions, and one step at a time. So to move forward three spaces, we would issue three `move forward` commands.
# 
# Additional commands are `move backward`, `move left`, `move right`. We also have a few other commands our robot understands: `pick` and `drop` for picking up and dropping objects it might find.

# We might write a command interpreter this way:

# Let's start by using some symbols to represent the robot's actions:

# In[9]:


symbols = {
    "F": "\u2192", 
    "B": "\u2190", 
    "L": "\u2191", 
    "R": "\u2193", 
    "pick": "\u2923", 
    "drop": "\u2925"
}

symbols


# In[10]:


def op(command):
    match command:
        case "move F":
            return symbols["F"]
        case "move B":
            return symbols["B"]
        case "move L":
            return symbols["L"]
        case "move R":
            return symbols["R"]
        case "pick":
            return symbols["pick"]
        case "drop":
            return symbols["drop"]
        case _:
            raise ValueError(f"{command} does not compute!")


# Then we could issue commands such as:

# In[11]:


op("move L")


# Or multiple sequences by maybe using a list of such commands, effectively creating a sequential program for our robot:

# In[12]:


[
    op("move F"),
    op("move F"),
    op("move L"),
    op("pick"),
    op("move R"),
    op("move L"),
    op("move F"),
    op("drop"),
]


# We could use something called **capturing** matched sub-patterns to simply our code somewhat:

# In[13]:


def op(command):
    match command:
        case ["move", ("F" | "B" | "L" |"R") as direction]:
            return symbols[direction]
        case "pick":
            return symbols["pick"]
        case "drop":
            return symvols["drop"]
        case _:
            raise ValueError(f"{command} does not compute!")


# In[14]:


op(["move", "L"])


# In[15]:


op("pick")


# In[16]:


try:
    op("fly")
except ValueError as ex:
    print(ex)


# This is kind of tedious, it would be nicer to write commands such as `move F F L` and `move R L F` instead.

# There are many ways we could solve this, but pattern matching on multiple values can be really useful here.

# In[17]:


def op(command):
    match command:
        case ['move', *directions]:
            return tuple(symbols[direction] for direction in directions)
        case "pick":
            return symbols["pick"]
        case "drop":
            return symbols["drop"]
        case _:
            raise ValueError(f"{command} does not compute!")


# What happens here is that the pattern matcher will recognize the first word `move` and then interpret the remaining words collection them in the `directions` variable (so this syntax is very similar to unpacking).

# We can now rewrite our program this way:

# In[18]:


[
    op(["move", "F", "F", "L"]),
    op("pick"),
    op(["move", "R", "L", "F"]),
    op("drop"),
]


# But now we have a slight problem:

# In[19]:


try:
    op(["move", "up"])
except Exception as ex:
    print(type(ex), ex)


# We would rather just get our custom `ValueError`. To do this we can place a **guard** on our `case` for the `move` command, that will not only do the match but also test an additional condition:

# In[20]:


def op(command):
    match command:
        case ['move', *directions] if set(directions) < symbols.keys():
            return tuple(symbols[direction] for direction in directions)
        case "pick":
            return symbols["pick"]
        case "drop":
            return symbols["drop"]
        case _:
            raise ValueError(f"{command} does not compute!")


# That `if ` statement (the **guard**) will only let the case block execute if the match is true **and** that `if` expression evaludates to `True`:

# In[21]:


try:
    op(["move", "up"])
except Exception as ex:
    print(type(ex), ex)


# There are many other ways we could have done this - probably better than this, but this was to illustrate how the multiple value matching can work!

# I urge you to read at least this [tutorial (pep 636)](https://peps.python.org/pep-0636/) on pattern matching.

# #### The `zip` Function

# We use the built-in `zip` function all the time. As we know, the `zip` will stop iterating after the first of the iterables provided in the arguments is exhausted:

# In[22]:


l1 = ['a', 'b', 'c']
l2 = [10, 20, 30, 40]

list(zip(l1, l2))


# As you can see the last element of `l2` is not included in the result since `l1` only had three elements.

# We can also use the `zip_longest` function in the `itertools` module to iterate over the longest iterable, providing some default value for any other iterable that has been exhausted:

# In[23]:


from itertools import zip_longest


# In[24]:


list(zip_longest(l1, l2, fillvalue='???'))


# But what if we want to only zip iterables that have the **same** length? We would need to test the length of each iterable first - but if those were iterators instead of iterables, we will have exhausted the iterator, and `zip` would come back "empty":

# In[25]:


l1 = (i ** 2 for i in range(4))
l2 = (i ** 3 for i in range(3))


# We could test to see if `l1` and `l2` are the same length:

# In[26]:


len(list(l1)) == len(list(l2))


# But, if we now try to `zip` them:

# In[27]:


list(zip(l1, l2))


# In Python 3.10, the `zip` function now has a keyword-only parameter called `strict` that will just do the zip, but throw an exception if one of the arguments get exhausted before the others:

# In[28]:


l1 = (i ** 2 for i in range(4))
l2 = (i ** 3 for i in range(3))

try:
    list(zip(l1, l2, strict=True))
except ValueError as ex:
    print(ex)


# And works just fine if the arguments all have the same length:

# In[29]:


l1 = (i ** 2 for i in range(4))
l2 = (i ** 3 for i in range(4))
l3 = (i ** 4 for i in range(4))

list(zip(l1, l2, l3))


# So why is this useful?

# In **many** cases, our code zips iterables that we expect to be of the same length. To avoid bugs in our program, we should check that this condition is true, otherwise zip will silently just zip based on the shortest one. But as we saw with iterators, that can be difficult to do without exhausting the very iterators we are trying to zip. (it can be done, it's just more code).

# So, if you are one of the lucky devs that gets to write Python 3.10 (or higher :-) ) code, you can just use `strict` whenever you zip things together and expect that they are all of the same length. Much easier to do it this way (and, as we discuss in Exception handling, falls into the category of "ask forgiveness later" which we saw was the preferred way (in general) to handle exceptions in our apps, as opposed to the "look before you leap" approach we would have to use to test the argument lengths.

# In[ ]:




