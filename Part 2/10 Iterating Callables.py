def counter():
    i = 0

    def inc():
        nonlocal i
        i += 1
        return i
    return inc


cnt = counter()

print(cnt())

print(cnt())


class CounterIterator:
    def __init__(self, counter_callable):
        self.counter_callable = counter_callable

    def __iter__(self):
        return self

    def __next__(self):
        return self.counter_callable()


cnt = counter()
cnt_iter = CounterIterator(cnt)
for _ in range(5):
    print(next(cnt_iter))

    # So basically we were able to create an iterator from some arbitrary callable.

    # But one issue is that we have an inifinite iterable.

    # One way around this issue, would be to specify a "stop" value when the iterator should decide to end the iteration.

    # Let's see how we would do this:


class CounterIterator:
    def __init__(self, counter_callable, sentinel):
        self.counter_callable = counter_callable
        self.sentinel = sentinel

    def __iter__(self):
        return self

    def __next__(self):
        result = self.counter_callable()
        if result == self.sentinel:
            raise StopIteration
        else:
            return result

# Now we can essentially provide a value that if returned from the callable will result in a StopIteration exception,
# # essentially terminating the iteration


cnt = counter()
cnt_iter = CounterIterator(cnt, 5)
for c in cnt_iter:
    print(c)

print(next(cnt_iter))

# We really should make sure the iterator has been consumed, so let's fix that:


class CounterIterator:
    def __init__(self, counter_callable, sentinel):
        self.counter_callable = counter_callable
        self.sentinel = sentinel
        self.is_consumed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_consumed:
            raise StopIteration
        else:
            result = self.counter_callable()
            if result == self.sentinel:
                self.is_consumed = True
                raise StopIteration
            else:
                return result


# Now it should behave as a normal iterator that cannot continue iterating once the first StopIteration exception has been raised
cnt = counter()
cnt_iter = CounterIterator(cnt, 5)
for c in cnt_iter:
    print(c)

print(next(cnt_iter))
