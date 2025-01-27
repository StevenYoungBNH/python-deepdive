#!/usr/bin/env python
# coding: utf-8

# ### Project 6 - Description

# The goal of this project is to rewrite the pull pipeline we created in the **Application - Pipelines - Pulling** video in the **Generators as Coroutines** section.
# 
# You should look at the techniques we used in the **Application - Pipelines - Broadcasting** video and apply them here.
# 
# The goal is to write a pipeline that will push data from the source file, `cars.csv`, and push it through some filters and a save coroutine to ultimately save the results as a csv file.
# 
# Try to make your code as generic as possible, and don't worry about column headers in the output file (unless you really want to!).

# When you are done with your solution you should be able to specify an arbitrary number of filters on the name field.
# 
# If you specify `Chevrolet`, `Carlo` and `Landau` for three filters, your output file should contain two lines of data only:

# ```
# Chevrolet Monte Carlo Landau,15.5,8,350.0,170.0,4165.,11.4,77,US
# Chevrolet Monte Carlo Landau,19.2,8,305.0,145.0,3425.,13.2,78,US
# ```

# Good luck!!
