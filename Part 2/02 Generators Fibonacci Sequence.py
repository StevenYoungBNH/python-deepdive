"""Here is the Fibonacci sequence:

1 1 2 3 5 8 13 ...

As you can see there is a recursive definition of the numbers in this sequence:

Fib(n) = Fib(n-1) + Fib(n-2)

where

Fib(0) = 1

and

Fib(1) = 1

Although we can certainly use a recursive approach to calculate the n-th number in the sequence, it is not a very
effective method - we can of course help it by using memoization, but we'll still run into Python's maximum recursion
depth. In Python there is a maximum number of times a recursive function can call itself (creating a stack frame at
every nested call) before Python gives us an exception that we have exceeded the maximum permitted depth (the number of
recursive calls). We can actually change that number if we want to, but if we're running into that limitation, it might
be better creating a non-recursive algorithm - recursion can be elegant, but not particularly efficient.
"""


from functools import lru_cache
from timeit import timeit


def fib_recursive(n):
    if n <= 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


print([fib_recursive(i) for i in range(7)])

print(timeit('fib_recursive(10)', globals=globals(), number=10))
print(timeit('fib_recursive(28)', globals=globals(), number=10))
print(timeit('fib_recursive(29)', globals=globals(), number=10))


print("========================================================================================")
print("                                  LRU CACHE                                             ")
print("========================================================================================")
# We can alleviate this by using memoization:


@lru_cache()
def fib_recursive(n):
    if n <= 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


print(timeit('fib_recursive(10)', globals=globals(), number=10))
print(timeit('fib_recursive(29)', globals=globals(), number=10))
# fib_recursive(2000) #  Recursion depth error at 1505 - program crashes when this line is executed
print(timeit('fib_recursive(500)', globals=globals(), number=10))


def fib(n):
    fib_0 = 1
    fib_1 = 1
    for i in range(n - 1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
    return fib_1


print([fib(i) for i in range(7)])

print(timeit('fib(5000)', globals=globals(), number=10))

# So now, let's create an iterator approach so we can iterate over the sequence, but without materializing it
# (i.e. we want to use lazy evaluation, not eager evaluation)

print("========================================================================================")
print("                                  ITERATOR                                              ")
print("========================================================================================")


class Fib:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        print("Fib.__iter__ called")
        return self.FibIter(self.n)

    class FibIter:
        def __init__(self, n):
            self.n = n
            self.i = 0

        def __iter__(self):
            print("FibIter.__iter__ called.")
            return self

        def __next__(self):
            # print(f"FibIter.__next__ called.")
            if self.i >= self.n:
                raise StopIteration
            else:
                result = fib(self.i)
                self.i += 1
                # print(f"Result: {result}")
                return result


fib_iterable = Fib(7)
for num in fib_iterable:
    print(num)


def fib_closure():
    i = 0

    def inner():
        nonlocal i
        result = fib(i)
        i += 1
        return result
    return inner


fib_numbers = fib_closure()
fib_iter = iter(fib_numbers, fib(7))
for num in fib_iter:
    print(num)
"""    
But there's two things here:

    The syntax for either implementation is a little convoluted and not very clear
    More importantly, notice what happens every time the next method is called - it has to calculate every Fibonacci number from scratch (using the fib function) - that is wasteful...

Instead, we can use a generator function very effectively here.

Here is our original fib function:
"""


def fib(n):
    fib_0 = 1
    fib_1 = 1
    for i in range(n - 1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
    return fib_1


print([fib(i) for i in range(7)])


def fib_gen(n):
    fib_0 = 1  # it's going to come up 2 short
    fib_1 = 1
    for i in range(n - 1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1


print([num for num in fib_gen(7)])


def fib_gen(n):
    fib_0 = 1
    yield fib_0
    fib_1 = 1
    yield fib_1
    for i in range(n - 1):
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1


print([num for num in fib_gen(7)])


def fib_gen(n):
    fib_0 = 1
    yield fib_0
    fib_1 = 1
    yield fib_1
    for i in range(n - 2):  # it was returning 1 too many
        fib_0, fib_1 = fib_1, fib_0 + fib_1
        yield fib_1


print([num for num in fib_gen(7)])

#  comparing the different methods

time1 = timeit('[num for num in Fib(5_000)]', globals=globals(), number=1)

#  closure
fib_numbers = fib_closure()
sentinel = fib(5_001)

time2 = timeit('[num for num in iter(fib_numbers, sentinel)]', globals=globals(), number=1)

time3 = timeit('[num for num in fib_gen(5_000)]', globals=globals(), number=1)

print(f"{time1:0.4f} {time2:0.4f} {time3:0.4f}")
