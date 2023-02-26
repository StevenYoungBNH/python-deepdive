class Cities:
    def __init__(self):
        self._cities = ['Paris', 'Berlin', 'Rome', 'Madrid', 'London']
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        else:
            item = self._cities[self._index]
            self._index += 1
            return item


cities = Cities()
print(list(enumerate(cities)))

cities = Cities()
sorted_cities = sorted(cities)
print(sorted_cities)


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)


class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


cities = Cities()

iter_1 = CityIterator(cities)

for city in iter_1:
    print(city)

iter_2 = CityIterator(cities)
i2 = [city.upper() for city in iter_2]
print(i2)

print("\n\nBeginning CitIterator2\n\n")


class CityIterator2:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self

    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


iter_1 = CityIterator2(cities)

for city in iter_1:
    print(city)


print("\n\nBeginning CitIterator3\n\n")


class CityIterator3:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0

    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self

    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            print("At StopIteration")
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator3(self)

    class CityIterator3:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                print("At StopIteration")
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item


cities = Cities()
print("Starting the for statement")
for city in cities:
    print(city)

print("Starting the 2nd for statement")
for city in cities:
    print(city)

print(list(enumerate(cities)))

iter_1 = iter(cities)
iter_2 = iter(cities)

print(id(iter_1), id(iter_2))

#  Making it both an iterable and a sequence type by adding 'getitem'.
print("\n\n========================================================================")
print("Now an iterable and a sequence type")
print("========================================================================")


class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']

    def __len__(self):
        return len(self._cities)

    def __getitem__(self, s):
        print('getting item...')
        return self._cities[s]

    # def __iter__(self):
        #print('Calling Cities instance __iter__')
        # return self.CityIterator(self)

    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0

        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self

        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item


cities = Cities()
print(cities[0])
print(cities[1])
print(cities[2])
print(cities[3])
# iterable
iter_city = iter(cities)
print(next(iter_city))
print(next(iter_city))
for ct, city in enumerate(cities):
    print(f"{ct}. {city}")


