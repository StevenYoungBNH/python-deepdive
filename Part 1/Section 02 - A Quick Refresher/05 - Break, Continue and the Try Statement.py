#!/usr/bin/env python
# coding: utf-8

# ### Loop Break and Continue inside a Try...Except...Finally

# Recall that in a ``try`` statement, the ``finally`` clause always runs:

# In[33]:


a = 10
b = 1
try:
    a / b
except ZeroDivisionError:
    print('division by 0')
finally:
    print('this always executes')


# In[34]:


a = 10
b = 0
try:
    a / b
except ZeroDivisionError:
    print('division by 0')
finally:
    print('this always executes')


# So, what happens when using a ``try`` statement within a ``while`` loop, and 
# a ``continue`` or ``break`` statement is encountered?

# In[47]:

# Added additional code, try except commenting in and out to answer a question
# where the else runs after exiting the loop 'Normally' not with a 'break' or 
# 'exceptioh. In conclusion if the loop is setup as "while True:" there will 
# never be a case where the else: will ever be executed. 

a = 0
b = 2

print("---------- The divide by 0 is handled outside the while loop. ----------")

try:
    
    while a < 3:
        print('-------------')
        a += 1
        b -= 1
        print(a / b)
    else:
        # This else clause will never execute due to the abnormal termination by 
        # exception. 
        
        print("In the else clause")
    # In[50]:
except ZeroDivisionError:
    print ("exited by division by 0")
    
    
print("---------- Handling the exception within the while loop. -----------")
a = 0
b = 2

try:
    
    while a < 3:
        print('-------------')
        a += 1
        b -= 1
        
        # Here the exception is going to be handled ingernally.
        # If all goes as planned the else clause should execute. 
        try:
            print(a / b)
            res = a / b
        except ZeroDivisionError:
            print(f'{a}, {b} - division by 0')
            res = 0
            continue # with the finally clause enabled, the continue will not loop
                     # to the top of the while. This results in the print of 
                     # the main loop executing. 
                     
        #finally:
            #print(f'{a}, {b} - always executes')
            # break
            
        print(f'{a}, {b} - main loop'.format(a, b))
    else:
        print("In the else clause")
    
    # As you can see in the above result, the ``finally`` code still 
    # executed, even
    # though the current iteration was cut short with the ``continue``
    # statement. 
    
    # This works the same with a ``break`` statement:
    
    # In[50]:
except ZeroDivisionError:
    print ("exited by division by 0")
finally:
    print("and here we are at the finally which will always occur")



a = 0
b = 2

while a < 3:
    print('-------------')
    a += 1
    b -= 1
    try:
        res = a / b
    except ZeroDivisionError:
        print(f'Line 122 {a}, {b} - division by 0')
        res = 0
        break
    finally:
        print(f'Line 126 {a}, {b} - always executes')
        
    print(f'Line 128 {a}, {b} - main loop')


# We can even combine all this with the ``else`` clause:

# In[54]:


a = 0
b = 2

while a < 3:
    print('-------------')
    a += 1
    b -= 1
    try:
        res = a / b
    except ZeroDivisionError:
        print(f'Line 146 {a}, {b} - division by 0')
        res = 0
        break # try commenting out the break, line 152 will be printed then. 
    finally:
        print(f'Line 150 {a}, {b} - finally always executes')
        
    print(f'Line 152 {a}, {b} - main loop')
else:
    print('\n\nno errors were encountered!') # Works because the errors were 
                                             # handled by exception. 


# In[55]:


a = 0
b = 5

while a < 3:
    print('-------------')
    a += 1
    b -= 1
    try:
        res = a / b
    except ZeroDivisionError:
        print(f'Line 171 {a}, {b} - division by 0')
        res = 0
        break
    finally:
        print(f'Line 175 {a}, {b} - always executes')
        
    print(f'Line 177 {a}, {b} - main loop')
else:
    print('\n\nno errors were encountered!')


# In[ ]:




